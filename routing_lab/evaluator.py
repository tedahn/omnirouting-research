"""Outcome-focused, deterministic evaluation of routing policies."""

from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from statistics import fmean
from typing import Any

from .router import route_request
from .store import LabStore


def _percentile(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    rank = (len(ordered) - 1) * percentile
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[lower]
    fraction = rank - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def _outcome_is_hard_valid(outcome: dict[str, Any], request: dict[str, Any]) -> bool:
    if outcome.get("policy_violation", False):
        return False
    if float(outcome["cost_usd"]) > float(request.get("max_cost_usd", float("inf"))):
        return False
    if float(outcome["latency_ms"]) > float(request.get("max_latency_ms", float("inf"))):
        return False
    return True


def _target_matches_request(model: dict[str, Any], request: dict[str, Any]) -> bool:
    if not model["enabled"] or model["kind"] != request["route_kind"]:
        return False
    if not set(request.get("required_capabilities", [])).issubset(model["capabilities"]):
        return False
    allowed = request.get("allowed_targets")
    if allowed is not None and model["id"] not in allowed:
        return False
    if model["id"] in request.get("blocked_targets", []):
        return False
    return True


def _objective(metrics: dict[str, Any], objective: dict[str, Any]) -> float:
    """Apply a versioned objective; raw metrics remain authoritative."""

    weights = objective["metric_weights"]
    return (
        float(weights["task_success"]) * float(metrics["task_success_rate"])
        - float(weights["hard_violation"]) * float(metrics["hard_violation_rate"])
        - float(weights["abstention"]) * float(metrics["abstention_rate"])
        - float(weights["oracle_regret"]) * float(metrics["mean_oracle_regret"])
        - float(weights["brier"]) * float(metrics["brier_score"])
        - float(weights["cost_utilization"]) * float(metrics["mean_cost_budget_utilization"])
        - float(weights["latency_utilization"]) * float(metrics["mean_latency_budget_utilization"])
    )


def evaluate_policy(
    store: LabStore,
    policy: dict[str, Any],
    *,
    objective: dict[str, Any] | None = None,
    suite: str = "development",
    partitions: set[str] | None = None,
    persist: bool = False,
    actor: str = "evaluator",
) -> dict[str, Any]:
    chosen_objective = objective or store.active_objective()
    cases = store.list("case", suite=suite)
    models = {model["id"]: model for model in store.list("model")}
    if partitions is not None:
        cases = [case for case in cases if case["partition"] in partitions]
    results: list[dict[str, Any]] = []

    for case in cases:
        request = case["request"]
        decision = route_request(
            store,
            request,
            policy=policy,
            predictions=case["predictions"],
            audit=False,
        )
        selected = decision["selected_target"]
        outcome = case["outcomes"].get(selected) if selected else None
        eligible_actual = {
            target_id: candidate
            for target_id, candidate in case["outcomes"].items()
            if target_id in models
            and _target_matches_request(models[target_id], request)
            and _outcome_is_hard_valid(candidate, request)
        }
        oracle_target = None
        oracle_quality = 0.0
        if eligible_actual:
            oracle_target, oracle_outcome = max(
                eligible_actual.items(),
                key=lambda item: (float(item[1]["quality"]), item[0]),
            )
            oracle_quality = float(oracle_outcome["quality"])
        actual_quality = float(outcome["quality"]) if outcome else 0.0
        predicted_probability = (
            float(decision["selected_prediction"]["pass_probability"])
            if decision["selected_prediction"]
            else 0.0
        )
        passed = bool(outcome and outcome["pass"])
        hard_violation = bool(outcome and not _outcome_is_hard_valid(outcome, request))
        cost_utilization = (
            float(outcome["cost_usd"]) / max(float(request["max_cost_usd"]), 1e-9)
            if outcome and "max_cost_usd" in request
            else 0.0
        )
        latency_utilization = (
            float(outcome["latency_ms"]) / max(float(request["max_latency_ms"]), 1e-9)
            if outcome and "max_latency_ms" in request
            else 0.0
        )
        results.append(
            {
                "case_id": case["id"],
                "partition": case["partition"],
                "selected_target": selected,
                "abstained": selected is None,
                "pass": passed,
                "quality": actual_quality,
                "cost_usd": float(outcome["cost_usd"]) if outcome else 0.0,
                "latency_ms": float(outcome["latency_ms"]) if outcome else 0.0,
                "hard_violation": hard_violation,
                "cost_budget_utilization": cost_utilization,
                "latency_budget_utilization": latency_utilization,
                "predicted_pass_probability": predicted_probability,
                "brier": (predicted_probability - float(passed)) ** 2,
                "oracle_target": oracle_target,
                "oracle_quality": oracle_quality,
                "oracle_regret": max(0.0, oracle_quality - actual_quality),
                "oracle_match": selected == oracle_target and oracle_target is not None,
                "decision_reason": decision["reason"],
            }
        )

    count = len(results)
    successes = sum(result["pass"] for result in results)
    costs = [result["cost_usd"] for result in results if not result["abstained"]]
    latencies = [result["latency_ms"] for result in results if not result["abstained"]]
    routed = [result for result in results if not result["abstained"]]
    metrics = {
        "case_count": count,
        "routed_count": sum(not result["abstained"] for result in results),
        "task_success_rate": successes / count if count else 0.0,
        "abstention_rate": sum(result["abstained"] for result in results) / count if count else 0.0,
        "hard_violation_rate": sum(result["hard_violation"] for result in results) / count if count else 0.0,
        "mean_quality": fmean(result["quality"] for result in results) if count else 0.0,
        "total_cost_usd": sum(costs),
        "cost_per_success_usd": sum(costs) / successes if successes else None,
        "latency_p50_ms": _percentile(latencies, 0.50),
        "latency_p95_ms": _percentile(latencies, 0.95),
        "latency_p99_ms": _percentile(latencies, 0.99),
        "mean_oracle_regret": fmean(result["oracle_regret"] for result in results) if count else 0.0,
        "oracle_selection_accuracy": (
            sum(result["oracle_match"] for result in results) / count if count else 0.0
        ),
        "brier_score": fmean(result["brier"] for result in results) if count else 0.0,
        "mean_cost_budget_utilization": (
            fmean(result["cost_budget_utilization"] for result in routed) if routed else 0.0
        ),
        "mean_latency_budget_utilization": (
            fmean(result["latency_budget_utilization"] for result in routed) if routed else 0.0
        ),
    }
    metrics["objective_score"] = _objective(metrics, chosen_objective)
    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "mode": "simulation_only",
        "suite": suite,
        "partitions": sorted(partitions) if partitions is not None else "all",
        "dataset_sha256": store.dataset_hash(suite),
        "evaluated_subset_sha256": store.collection_hash(cases),
        "policy_id": policy["id"],
        "policy_sha256": store.resource_hash(policy),
        "objective_id": chosen_objective["id"],
        "objective_sha256": store.resource_hash(chosen_objective),
        "objective_contract": chosen_objective,
        "metrics": metrics,
        "case_results": results,
        "limitations": [
            "Fixture outcomes are synthetic and do not establish live model performance.",
            "The composite objective is a development aid; raw metrics and hard guardrails govern comparison.",
        ],
    }
    if persist:
        store.initialize_runtime()
        identifier = f"eval-{policy['id']}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%fZ')}"
        path = store.runtime / "runs" / f"{identifier}.json"
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        report["artifact_path"] = str(path)
        store.audit(
            actor=actor,
            action="evaluation.completed",
            details={"policy_id": policy["id"], "suite": suite, "artifact_path": str(path)},
        )
    return report
