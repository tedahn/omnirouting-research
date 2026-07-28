#!/usr/bin/env python3
"""Validate the persistent structure of the OmniRouting research workspace."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROOT = {
    "README.md",
    "WORKSPACE_CHARTER.md",
    "CURRENT_STATE.md",
    "WORKSPACE_ORIGIN.md",
}
REQUIRED_RESEARCH = {
    "README.md",
    "NEXT_ACTION-001.md",
    "claims.csv",
    "sources.csv",
    "assumptions-forecasts.csv",
    "eval-cases.csv",
    "change-log.csv",
    "company-landscape.csv",
    "methodologies.csv",
    "outcomes.csv",
    "future-scenarios.csv",
    "METHODOLOGY-omni-routing.md",
    "RESEARCH_PLAN-2026-07-27.md",
    "briefs/RESEARCH_BRIEF-omnirouting.md",
    "profiles/README.md",
    "profiles/COMPANY_PROFILE_TEMPLATE.md",
    "decisions/README.md",
    "snapshots/README.md",
}


def main() -> int:
    errors: list[str] = []

    for name in sorted(REQUIRED_ROOT):
        path = ROOT / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            errors.append(f"Missing or empty root file: {name}")

    research = ROOT / "research"
    actual_research = {
        path.relative_to(research).as_posix()
        for path in research.rglob("*")
        if path.is_file()
    }
    missing_research = REQUIRED_RESEARCH - actual_research
    if missing_research:
        errors.append(f"Missing research state files: {sorted(missing_research)}")

    for path in research.glob("*.csv"):
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if not rows or not rows[0] or len(rows[0]) != len(set(rows[0])):
            errors.append(f"Invalid or duplicate CSV headers: {path.relative_to(ROOT)}")

    project = ROOT / "project"
    manifest_path = project / "MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid project manifest: {exc}")
        manifest = {}

    listed = manifest.get("files", [])
    if not isinstance(listed, list) or not all(isinstance(item, str) for item in listed):
        errors.append("Project manifest files must be a list of strings")
        listed = []
    for item in listed:
        pure = PurePosixPath(item)
        if pure.is_absolute() or ".." in pure.parts:
            errors.append(f"Unsafe project manifest path: {item}")

    actual_project = {
        path.relative_to(project).as_posix()
        for path in project.rglob("*")
        if path.is_file()
    }
    if set(listed) != actual_project:
        errors.append(
            "Project manifest mismatch: "
            f"missing={sorted(set(listed) - actual_project)}, "
            f"extra={sorted(actual_project - set(listed))}"
        )

    upload_path = project / "UPLOAD_MANIFEST.md"
    upload = upload_path.read_text(encoding="utf-8") if upload_path.is_file() else ""
    upload_section = upload.split("## Handbooks to upload", 1)[-1].split("## Templates", 1)[0]
    keep_local = upload.split("## Keep local", 1)[-1]
    if "PRE_UPLOAD_SAFETY.md" in upload_section:
        errors.append("Pre-upload safety is incorrectly listed for upload")
    if "PRE_UPLOAD_SAFETY.md" not in keep_local:
        errors.append("Pre-upload safety is missing from Keep local")

    for reference in re.findall(r"`((?:handbook|templates|\.\./)[^`]+)`", upload):
        target = (project / reference).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"Upload manifest reference escapes the workspace: {reference}")
            continue
        if not target.is_file():
            errors.append(f"Upload manifest reference is missing: {reference}")

    result = {
        "valid": not errors,
        "workspace": "OmniRouting Research Observatory",
        "project_files": len(actual_project),
        "research_files": len(actual_research),
        "errors": errors,
    }
    print(json.dumps(result))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
