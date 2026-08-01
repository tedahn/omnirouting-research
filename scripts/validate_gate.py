#!/usr/bin/env python3
"""Deterministically validate OmniRouting human gate records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ALLOWED_GATES = {f"G{i}" for i in range(7)}
ALLOWED_STATUSES = {
    "proposed",
    "in_review",
    "approved",
    "approved_with_conditions",
    "revised",
    "rejected",
    "deferred",
    "expired",
    "superseded",
}
DECIDED_STATUSES = ALLOWED_STATUSES - {"proposed", "in_review"}
REQUIRED_HEADERS = {
    "Gate",
    "Status",
    "Decision owner",
    "Requested by",
    "Opened at",
    "Decided at",
    "Expires at",
    "Supersedes",
    "Evidence snapshot",
}
REQUIRED_SECTIONS = {
    "Decision requested",
    "Why now",
    "In scope",
    "Out of scope",
    "Roles",
    "Evidence",
    "Acceptance criteria",
    "Stop conditions",
    "Decision",
    "Reversal evidence",
    "Handoff",
}
HEADER_PATTERN = re.compile(r"^- \*\*(?P<key>[^*]+?):\*\*\s*(?P<value>.*)$")
SECTION_PATTERN = re.compile(r"^##\s+(?P<name>.+?)\s*$")


def validate_gate(path: Path) -> dict[str, object]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {"path": str(path), "valid": False, "errors": [str(exc)]}

    headers: dict[str, str] = {}
    sections: set[str] = set()
    in_header = True
    for line in text.splitlines():
        section_match = SECTION_PATTERN.match(line)
        if section_match:
            in_header = False
            sections.add(section_match.group("name").strip())
            continue
        if in_header:
            header_match = HEADER_PATTERN.match(line)
            if header_match:
                headers[header_match.group("key").strip()] = header_match.group("value").strip()

    missing_headers = sorted(REQUIRED_HEADERS - headers.keys())
    missing_sections = sorted(REQUIRED_SECTIONS - sections)
    if missing_headers:
        errors.append(f"Missing headers: {', '.join(missing_headers)}")
    if missing_sections:
        errors.append(f"Missing sections: {', '.join(missing_sections)}")

    gate_token = headers.get("Gate", "").split(maxsplit=1)[0]
    if gate_token not in ALLOWED_GATES:
        errors.append(f"Invalid gate: {headers.get('Gate', '')!r}")

    status = headers.get("Status", "")
    if status not in ALLOWED_STATUSES:
        errors.append(f"Invalid status: {status!r}")

    owner = headers.get("Decision owner", "").strip().lower()
    if not owner or owner in {"unassigned", "unknown", "null", "n/a"}:
        errors.append("Decision owner must be a named human role or person")

    decided_at = headers.get("Decided at", "").strip().lower()
    is_null_decision = decided_at in {"", "null", "none", "n/a"}
    if status in {"proposed", "in_review"} and not is_null_decision:
        errors.append(f"Status {status!r} must not have a decision timestamp")
    if status in DECIDED_STATUSES and is_null_decision:
        errors.append(f"Status {status!r} requires a decision timestamp")

    snapshot = headers.get("Evidence snapshot", "").strip().lower()
    if not snapshot or snapshot in {"null", "none", "n/a"}:
        errors.append("Evidence snapshot must be versioned or explicitly hashed")
    else:
        snapshot_reference = re.search(r"`([^`]+)`", headers["Evidence snapshot"])
        if snapshot_reference:
            snapshot_path = (path.parent / snapshot_reference.group(1)).resolve()
            if not snapshot_path.is_file():
                errors.append(f"Evidence snapshot does not resolve: {snapshot_reference.group(1)}")
            else:
                declared_hash = re.search(
                    r"SHA-256\s+`([0-9a-fA-F]{64})`", headers["Evidence snapshot"]
                )
                if declared_hash:
                    actual_hash = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
                    if actual_hash.lower() != declared_hash.group(1).lower():
                        errors.append(
                            "Evidence snapshot hash mismatch: "
                            f"expected {declared_hash.group(1).lower()}, got {actual_hash}"
                        )

    if status == "proposed" and not re.search(
        r"\b(no new|zero) authority\b|\bgrants? no authority\b", text, re.IGNORECASE
    ):
        errors.append("A proposed gate must explicitly state that it grants no authority")

    return {
        "path": str(path),
        "gate": headers.get("Gate"),
        "status": status or None,
        "decision_owner": headers.get("Decision owner"),
        "valid": not errors,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Gate Markdown files")
    args = parser.parse_args()

    results = [validate_gate(path.resolve()) for path in args.paths]
    payload = {"valid": all(item["valid"] for item in results), "gates": results}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
