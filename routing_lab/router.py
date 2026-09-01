"""Deterministic routing for calls and agentic workflow stages."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from .contracts import (
    ContractError,
    validate_policy,
    validate_prediction,
    validate_request,
    validate_workflow,
)
from .store import LabStore


def _prediction(model: dict[str, Any], request: dict[str, Any], supplied: dict[str, Any]) -> dict[str, float]:
    if supplied:
        return {
            "pass_probability": float(supplied["pass_probability"]),
            "cost_usd": float(supplied["cost_usd"]),
            "latency_ms": float(supplied["latency_ms"]),
        }
    complexity = float(request["complexity"])
    affinity = float(model.get("complexity_affinity", 0.5))
    probability = float(model["quality_prior"]) - abs(complexity - affinity) * 0.25
    return {
        "pass_probability": max(0.0, min(1.0, probability)),
        "cost_usd": float(model["cost_usd"]) * (1 + complexity * 0.25),
        "latency_ms": float(model["latency_ms"]) * (1 + complexity * 0.35),
    }


def _base_exclusions(
    model: dict[str, Any],
    request: dict[str, Any],
    policy: dict[str, Any],
    prediction: dict[str, float],
) -> list[str]:
    reasons: list[str] = []
    target_id = model["id"]
    if not model["enabled"]:
        reasons.append("disabled")
    if model["kind"] != request["route_kind"]:
        reasons.append("wrong_route_kind")
    if model["kind"] not in policy["eligible_kinds"]:
        reasons.append("kind_blocked_by_policy")
    missing = sorted(set(request.get("required_capabilities", [])) - set(model["capabilities"]))
    if missing:
        reasons.append(f"missing_capabilities:{','.join(missing)}")
    allowed = request.get("allowed_targets")
    if allowed is not None and target_id not in allowed:
        reasons.append("not_in_allowed_targets")
    if target_id in request.get("blocked_targets", []):
        reasons.append("blocked_target")
    if prediction["cost_usd"] > float(request.get("max_cost_usd", float("inf"))):
        reasons.append("predicted_cost_exceeds_limit")
    if prediction["latency_ms"] > float(request.get("max_latency_ms", float("inf"))):
        reasons.append("predicted_latency_exceeds_limit")
    return reasons


def _score(policy: dict[str, Any], request: dict[str, Any], prediction: dict[str, float]) -> float:
    cost_limit = float(request.get("max_cost_usd", policy["normalization"]["cost_usd"]))
    latency_limit = float(request.get("max_latency_ms", policy["normalization"]["latency_ms"]))
    cost_efficiency = 1 - min(1.0, prediction["cost_usd"] / max(cost_limit, 1e-9))
    latency_efficiency = 1 - min(1.0, prediction["latency_ms"] / max(latency_limit, 1e-9))
    weights = policy["weights"]
    return (
        float(weights["quality"]) * prediction["pass_probability"]
        + float(weights["cost"]) * cost_efficiency
        + float(weights["latency"]) * latency_efficiency
    )


def route_request(
    store: LabStore,
    request: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
    predictions: dict[str, dict[str, Any]] | None = None,
    actor: str = "router",
    audit: bool = True,
) -> dict[str, Any]:
    """Select one target or explicitly abstain, preserving decision evidence."""

    validate_request(request)
    chosen_policy = deepcopy(policy or store.active_policy())
    validate_policy(chosen_policy)
    supplied_predictions = predictions or {}
    models = store.list("model")
    model_ids = {model["id"] for model in models}
    unknown_predictions = sorted(set(supplied_predictions) - model_ids)
    if unknown_predictions:
        raise ContractError(f"predictions reference unknown targets: {unknown_predictions}")
    for target_id, prediction in supplied_predictions.items():
        if not isinstance(prediction, dict):
            raise ContractError(f"predictions.{target_id} must be an object")
        validate_prediction(prediction, f"predictions.{target_id}")
    records: list[dict[str, Any]] = []

    for model in models:
        predicted = _prediction(model, request, supplied_predictions.get(model["id"], {}))
        exclusions = _base_exclusions(model, request, chosen_policy, predicted)
        record: dict[str, Any] = {
            "target_id": model["id"],
            "kind": model["kind"],
            "prediction": predicted,
            "excluded": bool(exclusions),
            "exclusion_reasons": exclusions,
            "score": None,
        }
        if not exclusions and chosen_policy["method"] == "score":
            floor = float(chosen_policy["quality_floor_by_risk"][request["risk"]])
            if predicted["pass_probability"] < floor:
                record["excluded"] = True
                record["exclusion_reasons"].append("below_risk_quality_floor")
            else:
                record["score"] = _score(chosen_policy, request, predicted)
        records.append(record)

    eligible = [record for record in records if not record["excluded"]]
    selection: dict[str, Any] | None = None
    reason = "no_eligible_target"

    if chosen_policy["method"] == "static":
        order = [chosen_policy["default_target"], chosen_policy["fallback_target"]]
        for target_id in order:
            selection = next(
                (record for record in eligible if record["target_id"] == target_id),
                None,
            )
            if selection is not None:
                reason = "static_default" if target_id == order[0] else "static_fallback"
                break
    elif eligible:
        selection = max(
            eligible,
            key=lambda record: (float(record["score"]), record["target_id"]),
        )
        if float(selection["score"]) < float(chosen_policy["abstain_below"]):
            selection = None
            reason = "best_score_below_abstention_threshold"
        else:
            reason = "highest_policy_score"

    decision = {
        "schema_version": "1.0",
        "request_id": request["id"],
        "policy_id": chosen_policy["id"],
        "route_kind": request["route_kind"],
        "selected_target": selection["target_id"] if selection else None,
        "abstained": selection is None,
        "reason": reason,
        "selected_prediction": selection["prediction"] if selection else None,
        "selected_score": selection["score"] if selection else None,
        "candidates": records,
    }
    if audit:
        store.audit(
            actor=actor,
            action="route.decision",
            details={
                "request_id": request["id"],
                "policy_id": chosen_policy["id"],
                "selected_target": decision["selected_target"],
                "reason": reason,
            },
        )
    return decision


def simulate_workflow(
    store: LabStore,
    workflow: dict[str, Any],
    input_request: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
    actor: str = "workflow-simulator",
    audit: bool = True,
) -> dict[str, Any]:
    """Route every stage independently using shared request context."""

    validate_workflow(workflow)
    if not isinstance(input_request, dict):
        raise ContractError("workflow input must be an object")
    raw_run_id = str(input_request.get("id", "run")).lower()
    run_id = re.sub(r"[^a-z0-9._-]+", "-", raw_run_id).strip("-.") or "run"
    stages: list[dict[str, Any]] = []
    stage_predictions = input_request.get("stage_predictions", {})
    if not isinstance(stage_predictions, dict):
        raise ContractError("workflow input stage_predictions must be an object")
    base_capabilities = input_request.get("required_capabilities", [])
    if not isinstance(base_capabilities, list) or not all(
        isinstance(item, str) and item for item in base_capabilities
    ):
        raise ContractError("workflow input required_capabilities must be an array of strings")

    for stage in workflow["stages"]:
        request = {
            "id": f"{workflow['id']}-{stage['id']}-{run_id}"[:128],
            "route_kind": stage["route_kind"],
            "required_capabilities": sorted(
                set(base_capabilities)
                | set(stage.get("required_capabilities", []))
            ),
            "complexity": float(input_request.get("complexity", 0.5)),
            "risk": input_request.get("risk", "medium"),
        }
        for optional in (
            "max_cost_usd",
            "max_latency_ms",
            "allowed_targets",
            "blocked_targets",
        ):
            if optional in input_request:
                request[optional] = input_request[optional]
        request.update(stage.get("request_overrides", {}))
        decision = route_request(
            store,
            request,
            policy=policy,
            predictions=stage_predictions.get(stage["id"], {}),
            actor=actor,
            audit=False,
        )
        stages.append({"stage_id": stage["id"], "request": request, "decision": decision})

    result = {
        "schema_version": "1.0",
        "workflow_id": workflow["id"],
        "policy_id": (policy or store.active_policy())["id"],
        "status": "completed" if all(not item["decision"]["abstained"] for item in stages) else "partial",
        "stages": stages,
    }
    if audit:
        store.audit(
            actor=actor,
            action="workflow.simulated",
            details={
                "workflow_id": workflow["id"],
                "status": result["status"],
                "stage_count": len(stages),
                "abstentions": sum(item["decision"]["abstained"] for item in stages),
            },
        )
    return result
