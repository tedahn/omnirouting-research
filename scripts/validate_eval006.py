#!/usr/bin/env python3
"""Validate EVAL-006 artifacts, hashes, synthetic metrics, and ledger isolation."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "validation" / "eval-006"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(path: Path, errors: list[str]) -> int:
    matched = 0
    if not path.is_file():
        errors.append(f"Missing manifest: {path.relative_to(ROOT)}")
        return matched

    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            errors.append(f"Malformed manifest line: {path.relative_to(ROOT)}:{number}")
            continue
        expected, relative = parts
        target = ROOT / relative.strip()
        if not target.is_file():
            errors.append(f"Missing hashed file: {relative.strip()}")
            continue
        actual = digest(target)
        if actual != expected:
            errors.append(f"Hash mismatch: {relative.strip()}")
            continue
        matched += 1
    return matched


def route_metrics(tasks: list[dict[str, object]], selector) -> dict[str, float | int]:
    successes = 0
    cost = 0
    latency = 0
    for task in tasks:
        model = selector(task)
        outcome = task[model]
        successes += int(outcome["success"])
        cost += int(outcome["cost_units"])
        latency += int(outcome["latency_ms"])
    count = len(tasks)
    return {
        "tasks": count,
        "successes": successes,
        "success_rate": successes / count,
        "total_cost_units": cost,
        "mean_latency_ms": latency / count,
    }


def main() -> int:
    errors: list[str] = []
    manifest_counts = {
        "frozen_inputs": verify_manifest(BASE / "FROZEN_INPUTS.sha256", errors),
        "scientific_ledgers": verify_manifest(
            BASE / "SCIENTIFIC_LEDGER_BASELINE.sha256", errors
        ),
        "preholdout": verify_manifest(
            BASE / "runner" / "PREHOLDOUT_ARTIFACTS.sha256", errors
        ),
        "runner": verify_manifest(BASE / "runner" / "ARTIFACTS.sha256", errors),
        "evaluator": verify_manifest(
            BASE / "evaluator" / "EVALUATOR_ARTIFACTS.sha256", errors
        ),
    }

    holdout = BASE / "fixture" / "holdout.json"
    commitment = BASE / "fixture" / "HOLDOUT_COMMITMENT.sha256"
    if not holdout.is_file() or not commitment.is_file():
        errors.append("Missing holdout or commitment")
        tasks: list[dict[str, object]] = []
    else:
        expected = commitment.read_text(encoding="utf-8").split(maxsplit=1)[0]
        if digest(holdout) != expected:
            errors.append("Holdout commitment mismatch")
        tasks = json.loads(holdout.read_text(encoding="utf-8"))["tasks"]

    observations_path = BASE / "runner" / "OBSERVATIONS.json"
    if observations_path.is_file() and tasks:
        observations = json.loads(observations_path.read_text(encoding="utf-8"))
        fixed = route_metrics(
            tasks, lambda task: "model_a" if task["complexity"] == "low" else "model_b"
        )
        always_a = route_metrics(tasks, lambda _task: "model_a")
        always_b = route_metrics(tasks, lambda _task: "model_b")
        expected_metrics = {
            "fixed_route": fixed,
            "always_model_a": always_a,
            "always_model_b": always_b,
        }
        for key, expected in expected_metrics.items():
            if observations.get(key) != expected:
                errors.append(f"Observed metric mismatch: {key}")

        reduction = (always_b["total_cost_units"] - fixed["total_cost_units"]) / always_b[
            "total_cost_units"
        ]
        if abs(reduction - 0.375) > 1e-12:
            errors.append("Unexpected cost reduction")
        if fixed["success_rate"] != 1 or fixed["mean_latency_ms"] >= always_b[
            "mean_latency_ms"
        ]:
            errors.append("Frozen positive-path criteria not met")
    else:
        errors.append("Missing observations or holdout tasks")

    case_path = BASE / "evaluator" / "CASE_RESULTS.json"
    if not case_path.is_file():
        errors.append("Missing evaluator case results")
        aggregate_status = None
        case_ids: set[str] = set()
    else:
        case_results = json.loads(case_path.read_text(encoding="utf-8"))
        aggregate_status = case_results.get("aggregate_status")
        cases = case_results.get("cases", [])
        case_ids = {case.get("case_id") for case in cases}
        required_ids = {"POS-01", "ADV-01", "ADV-02", "ADV-03", "ADV-04", "ADV-05", "ADV-06"}
        if case_ids != required_ids:
            errors.append("Evaluator case set mismatch")
        if any(not case.get("passed") for case in cases):
            errors.append("One or more evaluator cases failed")
        if aggregate_status != "model_checks_passed_pending_human_review":
            errors.append("Unexpected aggregate evaluator status")

    result_text = (BASE / "runner" / "VAL-RUN-006-01.md").read_text(encoding="utf-8")
    checkpoint_text = (BASE / "runner" / "VAL-CYCLE-006-01.md").read_text(
        encoding="utf-8"
    )
    for required_hash in (
        "3c39aa7e21a2643a24df2fddcf6407c88491291b60961c9e2cfa904bef667374",
        "a8512ca40fd2d8ece5a164ca86c06fe0339be80bab193b8ac3170f3188bec7b7",
    ):
        if required_hash not in result_text:
            errors.append(f"Result missing predecessor hash: {required_hash}")
    if "208e91aaf35aa9e9c4bf6c5a14ebf96e178e0c50b275db845934f7fc74db0e8e" not in checkpoint_text:
        errors.append("Checkpoint missing result hash")

    output = {
        "valid": not errors,
        "eval_case": "EVAL-006",
        "aggregate_status": aggregate_status,
        "manifest_matches": manifest_counts,
        "case_ids": sorted(case_id for case_id in case_ids if case_id),
        "errors": errors,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
