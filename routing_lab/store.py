"""Shared file workspace and append-only runtime audit log."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .contracts import ContractError, RESOURCE_KINDS, validate_id, validate_resource


class StoreError(RuntimeError):
    """Raised for safe workspace access failures."""


class LabStore:
    """Read and mutate the same JSON resources used by humans and agents."""

    def __init__(
        self,
        workspace: Path | str | None = None,
        runtime: Path | str | None = None,
    ) -> None:
        package_root = Path(__file__).resolve().parent
        self.workspace = Path(workspace or package_root / "workspace").resolve()
        configured_runtime = os.environ.get("OMNI_ROUTING_RUNTIME")
        self.runtime = Path(runtime or configured_runtime or package_root / "runtime").resolve()

    def initialize_runtime(self) -> None:
        for directory in ("events", "runs", "proposals", "completions"):
            (self.runtime / directory).mkdir(parents=True, exist_ok=True)

    def _directory(self, kind: str, suite: str | None = None) -> Path:
        if kind not in RESOURCE_KINDS:
            raise StoreError(f"unknown resource kind {kind!r}")
        if kind == "case":
            suite_id = validate_id(suite or "development", "suite")
            return self.workspace / "cases" / suite_id
        directories = {
            "model": "models",
            "policy": "policies",
            "workflow": "workflows",
            "objective": "objectives",
        }
        return self.workspace / directories[kind]

    def path_for(self, kind: str, resource_id: str, *, suite: str | None = None) -> Path:
        safe_id = validate_id(resource_id)
        path = (self._directory(kind, suite) / f"{safe_id}.json").resolve()
        try:
            path.relative_to(self.workspace)
        except ValueError as exc:
            raise StoreError("resource path escapes the workspace") from exc
        return path

    def list(self, kind: str, *, suite: str | None = None) -> list[dict[str, Any]]:
        directory = self._directory(kind, suite)
        if not directory.is_dir():
            return []
        resources = [self._read_path(path) for path in sorted(directory.glob("*.json"))]
        for resource in resources:
            validate_resource(kind, resource)
        return resources

    def get(self, kind: str, resource_id: str, *, suite: str | None = None) -> dict[str, Any]:
        path = self.path_for(kind, resource_id, suite=suite)
        if not path.is_file():
            raise StoreError(f"{kind} {resource_id!r} does not exist")
        resource = self._read_path(path)
        validate_resource(kind, resource)
        return resource

    def put(
        self,
        kind: str,
        resource: dict[str, Any],
        *,
        suite: str | None = None,
        actor: str = "unknown",
        allow_confirmation: bool = False,
    ) -> dict[str, Any]:
        validate_resource(kind, resource)
        self._guard_confirmation(kind, suite, allow_confirmation)
        path = self.path_for(kind, resource["id"], suite=suite)
        operation = "update" if path.exists() else "create"
        if operation == "update":
            self._guard_active_definition(kind, resource["id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        self._atomic_json_write(path, resource)
        self.audit(
            actor=actor,
            action=f"resource.{operation}",
            details={"kind": kind, "id": resource["id"], "suite": suite},
        )
        return {"operation": operation, "path": str(path), "resource": resource}

    def delete(
        self,
        kind: str,
        resource_id: str,
        *,
        suite: str | None = None,
        actor: str = "unknown",
        allow_confirmation: bool = False,
    ) -> dict[str, Any]:
        self._guard_confirmation(kind, suite, allow_confirmation)
        path = self.path_for(kind, resource_id, suite=suite)
        if not path.is_file():
            raise StoreError(f"{kind} {resource_id!r} does not exist")
        self._guard_active_definition(kind, resource_id)
        resource = self._read_path(path)
        path.unlink()
        self.audit(
            actor=actor,
            action="resource.delete",
            details={"kind": kind, "id": resource_id, "suite": suite},
        )
        return {"operation": "delete", "path": str(path), "resource": resource}

    def state(self) -> dict[str, Any]:
        path = self.workspace / "state.json"
        data = self._read_path(path)
        if data.get("mode") != "simulation_only":
            raise StoreError("workspace mode must remain simulation_only in this development harness")
        validate_id(data.get("active_policy"), "state.active_policy")
        validate_id(data.get("active_objective"), "state.active_objective")
        return data

    def write_state(self, state: dict[str, Any], *, actor: str) -> None:
        if state.get("mode") != "simulation_only":
            raise StoreError("this harness cannot activate live execution")
        validate_id(state.get("active_policy"), "state.active_policy")
        validate_id(state.get("active_objective"), "state.active_objective")
        self._atomic_json_write(self.workspace / "state.json", state)
        self.audit(actor=actor, action="state.update", details=state)

    def active_policy(self) -> dict[str, Any]:
        return self.get("policy", self.state()["active_policy"])

    def active_objective(self) -> dict[str, Any]:
        return self.get("objective", self.state()["active_objective"])

    def dataset_hash(self, suite: str) -> str:
        return self.collection_hash(self.list("case", suite=suite))

    @staticmethod
    def collection_hash(resources: list[dict[str, Any]]) -> str:
        digest = hashlib.sha256()
        for resource in sorted(resources, key=lambda item: item["id"]):
            digest.update(LabStore.canonical_json(resource).encode("utf-8"))
            digest.update(b"\n")
        return digest.hexdigest()

    @staticmethod
    def resource_hash(resource: dict[str, Any]) -> str:
        return hashlib.sha256(LabStore.canonical_json(resource).encode("utf-8")).hexdigest()

    @staticmethod
    def canonical_json(value: Any) -> str:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

    def audit(self, *, actor: str, action: str, details: dict[str, Any]) -> dict[str, Any]:
        self.initialize_runtime()
        event = {
            "schema_version": "1.0",
            "timestamp": datetime.now(UTC).isoformat(),
            "actor": actor,
            "action": action,
            "details": details,
        }
        path = self.runtime / "events" / "audit.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(self.canonical_json(event) + "\n")
        return event

    def recent_events(self, limit: int = 20) -> list[dict[str, Any]]:
        path = self.runtime / "events" / "audit.jsonl"
        if not path.is_file():
            return []
        lines = path.read_text(encoding="utf-8").splitlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]

    def validate_all(self) -> dict[str, Any]:
        errors: list[str] = []
        counts: dict[str, int] = {}
        for kind in ("model", "policy", "workflow", "objective"):
            try:
                counts[kind] = len(self.list(kind))
            except (ContractError, StoreError, json.JSONDecodeError) as exc:
                errors.append(f"{kind}: {exc}")
        cases = 0
        case_root = self.workspace / "cases"
        suites = sorted(path.name for path in case_root.iterdir() if path.is_dir())
        for suite in suites:
            try:
                suite_cases = self.list("case", suite=suite)
                cases += len(suite_cases)
                for case in suite_cases:
                    if suite == "confirmation" and case["partition"] != "confirmation":
                        errors.append(
                            f"case {case['id']}: confirmation suite requires confirmation partition"
                        )
                    if suite != "confirmation" and case["partition"] == "confirmation":
                        errors.append(
                            f"case {case['id']}: confirmation partition is outside confirmation suite"
                        )
            except (ContractError, StoreError, json.JSONDecodeError) as exc:
                errors.append(f"case suite {suite}: {exc}")
        counts["case"] = cases
        if not errors:
            models = {model["id"]: model for model in self.list("model")}
            for policy in self.list("policy"):
                for field in ("fallback_target", "default_target"):
                    target = policy.get(field)
                    if target is not None and target not in models:
                        errors.append(
                            f"policy {policy['id']}: {field} references missing target {target}"
                        )
            for suite in suites:
                for case in self.list("case", suite=suite):
                    missing = sorted(set(case["outcomes"]) - set(models))
                    if missing:
                        errors.append(
                            f"case {case['id']}: outcomes reference missing targets {missing}"
                        )
        try:
            state = self.state()
            self.get("policy", state["active_policy"])
            self.get("objective", state["active_objective"])
        except (ContractError, StoreError, json.JSONDecodeError) as exc:
            errors.append(f"state: {exc}")
        return {"valid": not errors, "counts": counts, "suites": suites, "errors": errors}

    @staticmethod
    def _guard_confirmation(kind: str, suite: str | None, allowed: bool) -> None:
        if kind == "case" and suite == "confirmation" and not allowed:
            raise StoreError(
                "confirmation cases are mutation-protected; pass explicit confirmation authorization"
            )

    def _guard_active_definition(self, kind: str, resource_id: str) -> None:
        state_field = {"policy": "active_policy", "objective": "active_objective"}.get(kind)
        if state_field and self.state()[state_field] == resource_id:
            raise StoreError(
                f"active {kind} {resource_id!r} cannot be changed through raw CRUD; "
                "create a new id and use the proposal path"
            )

    @staticmethod
    def _read_path(path: Path) -> dict[str, Any]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise StoreError(f"cannot read {path}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise StoreError(f"invalid JSON in {path}: {exc}") from exc
        if not isinstance(data, dict):
            raise StoreError(f"{path} must contain a JSON object")
        return data

    @staticmethod
    def _atomic_json_write(path: Path, data: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, sort_keys=True, ensure_ascii=False)
                handle.write("\n")
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
