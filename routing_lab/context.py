"""Dynamic context injection for routing-lab operators."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .store import LabStore


def capability_map() -> dict[str, Any]:
    path = Path(__file__).resolve().parent / "CAPABILITY_MAP.json"
    return json.loads(path.read_text(encoding="utf-8"))


def build_context(store: LabStore) -> dict[str, Any]:
    state = store.state()
    return {
        "schema_version": "1.0",
        "mode": state["mode"],
        "active_policy": state["active_policy"],
        "active_objective": state["active_objective"],
        "models": [
            {
                "id": model["id"],
                "kind": model["kind"],
                "provider": model["provider"],
                "capabilities": model["capabilities"],
                "enabled": model["enabled"],
            }
            for model in store.list("model")
        ],
        "policies": [policy["id"] for policy in store.list("policy")],
        "workflows": [workflow["id"] for workflow in store.list("workflow")],
        "objectives": [objective["id"] for objective in store.list("objective")],
        "case_suites": {
            path.name: len(store.list("case", suite=path.name))
            for path in sorted((store.workspace / "cases").iterdir())
            if path.is_dir()
        },
        "capabilities": capability_map()["actions"],
        "recent_activity": store.recent_events(limit=10),
        "boundaries": [
            "Simulation only: no provider API calls are implemented or authorized.",
            "Optimization may use development train/validation partitions only.",
            "Confirmation data is mutation-protected and cannot be used by the optimizer.",
            "Applying a proposal changes only local simulation state and requires a named human.",
        ],
    }
