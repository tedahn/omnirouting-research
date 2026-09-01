"""Validation contracts for routing-lab resources.

The contracts intentionally use ordinary JSON-compatible dictionaries. Agents can
inspect and edit the same records humans use without a generated client or hidden
database schema.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable
from typing import Any


class ContractError(ValueError):
    """Raised when a resource violates an inspectable lab contract."""


RESOURCE_KINDS = ("model", "policy", "workflow", "case", "objective")
ROUTE_KINDS = ("model", "agent")
RISK_LEVELS = ("low", "medium", "high", "critical")
POLICY_METHODS = ("static", "score")
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")


def _mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{field} must be an object")
    return value


def _list(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError(f"{field} must be an array")
    return value


def _string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be a non-empty string")
    return value


def _number(value: Any, field: str, *, minimum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractError(f"{field} must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise ContractError(f"{field} must be finite")
    if minimum is not None and result < minimum:
        raise ContractError(f"{field} must be >= {minimum}")
    return result


def validate_id(value: Any, field: str = "id") -> str:
    result = _string(value, field)
    if not SAFE_ID.fullmatch(result):
        raise ContractError(
            f"{field} must match {SAFE_ID.pattern}; got {result!r}"
        )
    return result


def validate_model(data: dict[str, Any]) -> None:
    validate_id(data.get("id"))
    if data.get("kind") not in ROUTE_KINDS:
        raise ContractError(f"model.kind must be one of {ROUTE_KINDS}")
    _string(data.get("provider"), "model.provider")
    capabilities = _list(data.get("capabilities"), "model.capabilities")
    if not capabilities or not all(isinstance(item, str) and item for item in capabilities):
        raise ContractError("model.capabilities must contain non-empty strings")
    quality = _number(data.get("quality_prior"), "model.quality_prior", minimum=0)
    if quality > 1:
        raise ContractError("model.quality_prior must be <= 1")
    _number(data.get("cost_usd"), "model.cost_usd", minimum=0)
    _number(data.get("latency_ms"), "model.latency_ms", minimum=0)
    if not isinstance(data.get("enabled"), bool):
        raise ContractError("model.enabled must be boolean")


def validate_policy(data: dict[str, Any]) -> None:
    validate_id(data.get("id"))
    method = data.get("method")
    if method not in POLICY_METHODS:
        raise ContractError(f"policy.method must be one of {POLICY_METHODS}")
    validate_id(data.get("fallback_target"), "policy.fallback_target")
    eligible = _list(data.get("eligible_kinds"), "policy.eligible_kinds")
    if not eligible or any(item not in ROUTE_KINDS for item in eligible):
        raise ContractError(f"policy.eligible_kinds must use {ROUTE_KINDS}")
    normalization = _mapping(data.get("normalization"), "policy.normalization")
    if set(normalization) != {"cost_usd", "latency_ms"}:
        raise ContractError(
            "policy.normalization must contain exactly cost_usd and latency_ms"
        )
    for key, value in normalization.items():
        if _number(value, f"policy.normalization.{key}", minimum=0) == 0:
            raise ContractError(f"policy.normalization.{key} must be > 0")
    if method == "static":
        validate_id(data.get("default_target"), "policy.default_target")
    else:
        weights = _mapping(data.get("weights"), "policy.weights")
        required = {"quality", "cost", "latency"}
        if set(weights) != required:
            raise ContractError(f"policy.weights must contain exactly {sorted(required)}")
        values = [_number(weights[key], f"policy.weights.{key}", minimum=0) for key in required]
        if not math.isclose(sum(values), 1.0, abs_tol=1e-9):
            raise ContractError("policy.weights must sum to 1")
        threshold = _number(data.get("abstain_below"), "policy.abstain_below", minimum=0)
        if threshold > 1:
            raise ContractError("policy.abstain_below must be <= 1")
        floors = _mapping(data.get("quality_floor_by_risk"), "policy.quality_floor_by_risk")
        if set(floors) != set(RISK_LEVELS):
            raise ContractError(
                f"policy.quality_floor_by_risk must contain exactly {list(RISK_LEVELS)}"
            )
        for risk, value in floors.items():
            floor = _number(value, f"policy.quality_floor_by_risk.{risk}", minimum=0)
            if floor > 1:
                raise ContractError(f"quality floor for {risk} must be <= 1")


def validate_request(data: dict[str, Any], *, field: str = "request") -> None:
    validate_id(data.get("id"), f"{field}.id")
    if data.get("route_kind") not in ROUTE_KINDS:
        raise ContractError(f"{field}.route_kind must be one of {ROUTE_KINDS}")
    required = _list(data.get("required_capabilities", []), f"{field}.required_capabilities")
    if not all(isinstance(item, str) and item for item in required):
        raise ContractError(f"{field}.required_capabilities must contain strings")
    complexity = _number(data.get("complexity"), f"{field}.complexity", minimum=0)
    if complexity > 1:
        raise ContractError(f"{field}.complexity must be <= 1")
    if data.get("risk") not in RISK_LEVELS:
        raise ContractError(f"{field}.risk must be one of {RISK_LEVELS}")
    for optional in ("max_cost_usd", "max_latency_ms"):
        if optional in data:
            _number(data[optional], f"{field}.{optional}", minimum=0)
    for optional in ("allowed_targets", "blocked_targets"):
        if optional in data:
            items = _list(data[optional], f"{field}.{optional}")
            for item in items:
                validate_id(item, f"{field}.{optional} item")


def validate_outcome(data: dict[str, Any], field: str) -> None:
    if not isinstance(data.get("pass"), bool):
        raise ContractError(f"{field}.pass must be boolean")
    quality = _number(data.get("quality"), f"{field}.quality", minimum=0)
    if quality > 1:
        raise ContractError(f"{field}.quality must be <= 1")
    _number(data.get("cost_usd"), f"{field}.cost_usd", minimum=0)
    _number(data.get("latency_ms"), f"{field}.latency_ms", minimum=0)
    if "policy_violation" in data and not isinstance(data["policy_violation"], bool):
        raise ContractError(f"{field}.policy_violation must be boolean")


def validate_prediction(data: dict[str, Any], field: str) -> None:
    probability = _number(data.get("pass_probability"), f"{field}.pass_probability", minimum=0)
    if probability > 1:
        raise ContractError(f"{field}.pass_probability must be <= 1")
    _number(data.get("cost_usd"), f"{field}.cost_usd", minimum=0)
    _number(data.get("latency_ms"), f"{field}.latency_ms", minimum=0)


def validate_case(data: dict[str, Any]) -> None:
    validate_id(data.get("id"))
    if data.get("partition") not in ("train", "validation", "confirmation"):
        raise ContractError("case.partition must be train, validation, or confirmation")
    request = _mapping(data.get("request"), "case.request")
    validate_request(request, field="case.request")
    if request.get("id") != data.get("id"):
        raise ContractError("case.id and case.request.id must match")
    outcomes = _mapping(data.get("outcomes"), "case.outcomes")
    predictions = _mapping(data.get("predictions"), "case.predictions")
    if not outcomes:
        raise ContractError("case.outcomes must not be empty")
    if set(outcomes) != set(predictions):
        raise ContractError("case outcomes and predictions must have identical target ids")
    for target_id, outcome in outcomes.items():
        validate_id(target_id, "case outcome target id")
        validate_outcome(_mapping(outcome, f"case.outcomes.{target_id}"), f"case.outcomes.{target_id}")
        validate_prediction(
            _mapping(predictions[target_id], f"case.predictions.{target_id}"),
            f"case.predictions.{target_id}",
        )


def validate_workflow(data: dict[str, Any]) -> None:
    validate_id(data.get("id"))
    stages = _list(data.get("stages"), "workflow.stages")
    if not stages:
        raise ContractError("workflow.stages must not be empty")
    seen: set[str] = set()
    for index, raw_stage in enumerate(stages):
        stage = _mapping(raw_stage, f"workflow.stages[{index}]")
        stage_id = validate_id(stage.get("id"), f"workflow.stages[{index}].id")
        if stage_id in seen:
            raise ContractError(f"duplicate workflow stage id: {stage_id}")
        seen.add(stage_id)
        if stage.get("route_kind") not in ROUTE_KINDS:
            raise ContractError(f"workflow stage {stage_id} has invalid route_kind")
        required = _list(
            stage.get("required_capabilities", []),
            f"workflow.stages[{index}].required_capabilities",
        )
        if not all(isinstance(item, str) and item for item in required):
            raise ContractError(f"workflow stage {stage_id} capabilities must be strings")
        overrides = _mapping(stage.get("request_overrides", {}), f"workflow stage {stage_id} overrides")
        if "complexity" in overrides:
            value = _number(overrides["complexity"], f"workflow stage {stage_id} complexity", minimum=0)
            if value > 1:
                raise ContractError(f"workflow stage {stage_id} complexity must be <= 1")
        if "risk" in overrides and overrides["risk"] not in RISK_LEVELS:
            raise ContractError(f"workflow stage {stage_id} has invalid risk")


def validate_objective(data: dict[str, Any]) -> None:
    validate_id(data.get("id"))
    weights = _mapping(data.get("metric_weights"), "objective.metric_weights")
    required = {
        "task_success",
        "hard_violation",
        "abstention",
        "oracle_regret",
        "brier",
        "cost_utilization",
        "latency_utilization",
    }
    if set(weights) != required:
        raise ContractError(
            f"objective.metric_weights must contain exactly {sorted(required)}"
        )
    for key, value in weights.items():
        _number(value, f"objective.metric_weights.{key}", minimum=0)
    guardrails = _mapping(data.get("hard_guardrails"), "objective.hard_guardrails")
    if set(guardrails) != {"max_hard_violation_rate", "max_success_regression"}:
        raise ContractError(
            "objective.hard_guardrails must contain max_hard_violation_rate and max_success_regression"
        )
    for key, value in guardrails.items():
        number = _number(value, f"objective.hard_guardrails.{key}", minimum=0)
        if number > 1:
            raise ContractError(f"objective.hard_guardrails.{key} must be <= 1")
    _number(data.get("meaningful_improvement"), "objective.meaningful_improvement", minimum=0)


VALIDATORS: dict[str, Callable[[dict[str, Any]], None]] = {
    "model": validate_model,
    "policy": validate_policy,
    "workflow": validate_workflow,
    "case": validate_case,
    "objective": validate_objective,
}


def validate_resource(kind: str, data: dict[str, Any]) -> None:
    if kind not in VALIDATORS:
        raise ContractError(f"unknown resource kind {kind!r}; expected one of {RESOURCE_KINDS}")
    if not isinstance(data, dict):
        raise ContractError(f"{kind} resource must be a JSON object")
    VALIDATORS[kind](data)
