"""Stable JSON CLI for humans and agents."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .context import build_context, capability_map
from .contracts import ContractError, RESOURCE_KINDS
from .evaluator import evaluate_policy
from .optimizer import (
    apply_proposal,
    delete_proposal,
    list_proposals,
    optimize_policy,
    read_proposal,
)
from .router import route_request, simulate_workflow
from .store import LabStore, StoreError


def _json_file(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ContractError(f"{path} must contain a JSON object")
    return data


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python3 -m routing_lab")
    parser.add_argument("--workspace", help="Override the shared workspace directory")
    parser.add_argument("--runtime", help="Override the untracked runtime directory")
    parser.add_argument("--actor", default="cli-operator", help="Audit actor identifier")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("init", help="Create untracked runtime directories")
    commands.add_parser("validate", help="Validate every workspace resource")
    commands.add_parser("capabilities", help="Show the complete action parity map")
    commands.add_parser("context", help="Show dynamic state and capability context")

    resource = commands.add_parser("resource", help="Atomic resource CRUD")
    resource_commands = resource.add_subparsers(dest="resource_command", required=True)
    resource_list = resource_commands.add_parser("list")
    resource_list.add_argument("kind", choices=RESOURCE_KINDS)
    resource_list.add_argument("--suite", default="development")
    resource_list.add_argument("--allow-confirmation", action="store_true")
    resource_get = resource_commands.add_parser("get")
    resource_get.add_argument("kind", choices=RESOURCE_KINDS)
    resource_get.add_argument("id")
    resource_get.add_argument("--suite", default="development")
    resource_get.add_argument("--allow-confirmation", action="store_true")
    resource_put = resource_commands.add_parser("put")
    resource_put.add_argument("kind", choices=RESOURCE_KINDS)
    resource_put.add_argument("file")
    resource_put.add_argument("--suite", default="development")
    resource_put.add_argument("--allow-confirmation", action="store_true")
    resource_delete = resource_commands.add_parser("delete")
    resource_delete.add_argument("kind", choices=RESOURCE_KINDS)
    resource_delete.add_argument("id")
    resource_delete.add_argument("--suite", default="development")
    resource_delete.add_argument("--allow-confirmation", action="store_true")
    resource_delete.add_argument("--yes", action="store_true")

    route = commands.add_parser("route", help="Route one model or agent request")
    route.add_argument("--request", required=True, help="JSON request file")
    route.add_argument("--policy", help="Policy id; defaults to active policy")
    route.add_argument("--predictions", help="Optional JSON target-prediction object")

    workflow = commands.add_parser("workflow", help="Simulate an agentic workflow")
    workflow.add_argument("id")
    workflow.add_argument("--input", required=True, help="JSON workflow input file")
    workflow.add_argument("--policy", help="Policy id; defaults to active policy")

    evaluate = commands.add_parser("evaluate", help="Evaluate a policy on a frozen suite")
    evaluate.add_argument("--policy", help="Policy id; defaults to active policy")
    evaluate.add_argument("--objective", help="Objective id; defaults to active objective")
    evaluate.add_argument("--suite", default="development")
    evaluate.add_argument("--partition", action="append", choices=("train", "validation", "confirmation"))
    evaluate.add_argument("--allow-confirmation", action="store_true")
    evaluate.add_argument("--no-persist", action="store_true")

    optimize = commands.add_parser("optimize", help="Search development data and create a proposal")
    optimize.add_argument("--base-policy", help="Policy id; defaults to active policy")
    optimize.add_argument("--objective", help="Objective id; defaults to active objective")
    optimize.add_argument("--suite", default="development")

    proposal = commands.add_parser("proposal", help="Inspect or manage optimizer proposals")
    proposal_commands = proposal.add_subparsers(dest="proposal_command", required=True)
    proposal_commands.add_parser("list")
    proposal_show = proposal_commands.add_parser("show")
    proposal_show.add_argument("id")
    proposal_apply = proposal_commands.add_parser("apply")
    proposal_apply.add_argument("id")
    proposal_apply.add_argument("--approved-by", required=True)
    proposal_delete = proposal_commands.add_parser("delete")
    proposal_delete.add_argument("id")
    proposal_delete.add_argument("--yes", action="store_true")

    complete = commands.add_parser("complete-task", help="Explicitly record task completion")
    complete.add_argument("--summary", required=True)
    complete.add_argument("--evidence", action="append", default=[])
    return parser


def _suite(kind: str, suite: str) -> str | None:
    return suite if kind == "case" else None


def _execute(args: argparse.Namespace, store: LabStore) -> dict[str, Any] | list[Any]:
    if args.command == "init":
        store.initialize_runtime()
        return {"initialized": True, "runtime": str(store.runtime), "mode": store.state()["mode"]}
    if args.command == "validate":
        result = store.validate_all()
        if not result["valid"]:
            raise StoreError(f"workspace validation failed: {result['errors']}")
        return result
    if args.command == "capabilities":
        return capability_map()
    if args.command == "context":
        return build_context(store)
    if args.command == "resource":
        suite = _suite(args.kind, args.suite)
        if (
            args.kind == "case"
            and suite == "confirmation"
            and args.resource_command in {"list", "get"}
            and not args.allow_confirmation
        ):
            raise StoreError("confirmation case access requires --allow-confirmation")
        if args.resource_command == "list":
            return {"kind": args.kind, "suite": suite, "resources": store.list(args.kind, suite=suite)}
        if args.resource_command == "get":
            return store.get(args.kind, args.id, suite=suite)
        if args.resource_command == "put":
            return store.put(
                args.kind,
                _json_file(args.file),
                suite=suite,
                actor=args.actor,
                allow_confirmation=args.allow_confirmation,
            )
        if args.resource_command == "delete":
            if not args.yes:
                raise StoreError("resource deletion requires --yes")
            return store.delete(
                args.kind,
                args.id,
                suite=suite,
                actor=args.actor,
                allow_confirmation=args.allow_confirmation,
            )
    if args.command == "route":
        policy = store.get("policy", args.policy) if args.policy else store.active_policy()
        predictions = _json_file(args.predictions) if args.predictions else None
        return route_request(
            store,
            _json_file(args.request),
            policy=policy,
            predictions=predictions,
            actor=args.actor,
        )
    if args.command == "workflow":
        policy = store.get("policy", args.policy) if args.policy else store.active_policy()
        return simulate_workflow(
            store,
            store.get("workflow", args.id),
            _json_file(args.input),
            policy=policy,
            actor=args.actor,
        )
    if args.command == "evaluate":
        if args.suite == "confirmation" and not args.allow_confirmation:
            raise StoreError("confirmation evaluation requires --allow-confirmation")
        policy = store.get("policy", args.policy) if args.policy else store.active_policy()
        objective = (
            store.get("objective", args.objective) if args.objective else store.active_objective()
        )
        return evaluate_policy(
            store,
            policy,
            objective=objective,
            suite=args.suite,
            partitions=set(args.partition) if args.partition else None,
            persist=not args.no_persist,
            actor=args.actor,
        )
    if args.command == "optimize":
        policy = store.get("policy", args.base_policy) if args.base_policy else store.active_policy()
        objective = (
            store.get("objective", args.objective) if args.objective else store.active_objective()
        )
        return optimize_policy(
            store,
            policy,
            objective=objective,
            suite=args.suite,
            actor=args.actor,
        )
    if args.command == "proposal":
        if args.proposal_command == "list":
            return {"proposals": list_proposals(store)}
        if args.proposal_command == "show":
            return read_proposal(store, args.id)
        if args.proposal_command == "apply":
            return apply_proposal(store, args.id, approved_by=args.approved_by)
        if args.proposal_command == "delete":
            if not args.yes:
                raise StoreError("proposal deletion requires --yes")
            return delete_proposal(store, args.id, actor=args.actor)
    if args.command == "complete-task":
        store.initialize_runtime()
        completion = {
            "schema_version": "1.0",
            "completed_at": datetime.now(UTC).isoformat(),
            "actor": args.actor,
            "summary": args.summary,
            "evidence": args.evidence,
        }
        identifier = f"completion-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%fZ')}"
        path = store.runtime / "completions" / f"{identifier}.json"
        path.write_text(json.dumps(completion, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        completion["artifact_path"] = str(path)
        store.audit(actor=args.actor, action="task.completed", details=completion)
        return completion
    raise StoreError("unhandled command")


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    store = LabStore(workspace=args.workspace, runtime=args.runtime)
    try:
        result = _execute(args, store)
    except (ContractError, StoreError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, "result": result}, indent=2, sort_keys=True))
    return 0
