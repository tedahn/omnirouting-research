#!/usr/bin/env python3
"""Validate the append-only, hash-chained human-gate handoff event ledger."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

from validate_gate import validate_gate


EXPECTED_HEADERS = [
    "event_id",
    "handoff_id",
    "gate_id",
    "decision_hash",
    "event_type",
    "event_at",
    "execution_count",
    "owner",
    "authorized_action",
    "budget",
    "expires_at",
    "stop_conditions",
    "required_output",
    "validation",
    "reason",
    "notes",
    "previous_event_hash",
    "event_hash",
]
TERMINAL_EVENTS = {"consumed", "expired", "revoked"}
ALLOWED_EVENTS = {"issued", *TERMINAL_EVENTS}
APPROVED_STATUSES = {"approved", "approved_with_conditions"}
EVENT_ID_PATTERN = re.compile(r"^EVENT-[0-9]{3,}$")
HANDOFF_ID_PATTERN = re.compile(r"^HANDOFF-[0-9]{3,}$")
GATE_ID_PATTERN = re.compile(r"^GATE-[0-9]{3,}$")
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
CHECKPOINT_ID_PATTERN = re.compile(r"^CHECKPOINT-[0-9]{3,}$")
CHECKPOINT_STATUSES = {"pending_human_signature", "trusted", "superseded"}


def gate_id_from_path(path: Path) -> str:
    parts = path.stem.split("-", 2)
    return "-".join(parts[:2])


def compute_event_hash(row: dict[str, str]) -> str:
    payload = {key: row.get(key, "") for key in EXPECTED_HEADERS if key != "event_hash"}
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_handoffs(
    ledger: Path,
    decisions: Path,
    head_file: Path | None = None,
    checkpoint_file: Path | None = None,
) -> dict[str, object]:
    errors: list[str] = []
    head_file = head_file or ledger.with_name("handoff-ledger-head.json")
    checkpoint_file = checkpoint_file or ledger.with_name(
        "trusted-handoff-checkpoints.json"
    )
    try:
        with ledger.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames or []
            rows = [{key: value or "" for key, value in row.items()} for row in reader]
    except OSError as exc:
        return {"valid": False, "errors": [str(exc)], "handoffs": []}

    try:
        head = json.loads(head_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "valid": False,
            "errors": [f"Invalid handoff ledger head: {exc}"],
            "handoffs": [],
        }

    try:
        checkpoint_document = json.loads(checkpoint_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "valid": False,
            "errors": [f"Invalid trusted handoff checkpoints: {exc}"],
            "handoffs": [],
            "checkpoints": [],
        }

    if not isinstance(checkpoint_document, dict):
        errors.append("Trusted handoff checkpoint document must be an object")
        checkpoint_document = {}
    checkpoints = checkpoint_document.get("checkpoints", [])
    if checkpoint_document.get("version") != 1:
        errors.append("Unsupported trusted handoff checkpoint version")
    if not isinstance(checkpoints, list) or not checkpoints:
        errors.append("At least one trusted handoff checkpoint record is required")
        checkpoints = []

    if headers != EXPECTED_HEADERS:
        errors.append(f"Invalid handoff event headers: {headers!r}")

    gate_files = sorted(decisions.glob("GATE-*.md"))
    gate_records: dict[str, dict[str, object]] = {}
    gate_hashes: dict[str, str] = {}
    for gate_file in gate_files:
        gate_id = gate_id_from_path(gate_file)
        gate_records[gate_id] = validate_gate(gate_file)
        gate_hashes[gate_id] = hashlib.sha256(gate_file.read_bytes()).hexdigest()

    seen_event_ids: set[str] = set()
    seen_handoff_ids: set[str] = set()
    issued_gates: set[str] = set()
    issued_decisions: set[tuple[str, str]] = set()
    state_by_handoff: dict[str, dict[str, object]] = {}
    issuance_positions: list[tuple[str, str, int]] = []
    previous_hash = ""

    required_event_fields = [
        "event_at",
        "owner",
        "authorized_action",
        "budget",
        "expires_at",
        "stop_conditions",
        "required_output",
        "validation",
        "reason",
    ]

    for line_number, row in enumerate(rows, start=2):
        prefix = f"handoffs.csv:{line_number}"
        event_id = row["event_id"].strip()
        handoff_id = row["handoff_id"].strip()
        gate_id = row["gate_id"].strip()
        decision_hash = row["decision_hash"].strip().lower()
        event_type = row["event_type"].strip()
        declared_previous = row["previous_event_hash"].strip().lower()
        declared_event_hash = row["event_hash"].strip().lower()

        if not EVENT_ID_PATTERN.fullmatch(event_id):
            errors.append(f"{prefix}: invalid event_id {event_id!r}")
        if event_id in seen_event_ids:
            errors.append(f"{prefix}: duplicate event_id {event_id}")
        seen_event_ids.add(event_id)

        if not HANDOFF_ID_PATTERN.fullmatch(handoff_id):
            errors.append(f"{prefix}: invalid handoff_id {handoff_id!r}")
        if not GATE_ID_PATTERN.fullmatch(gate_id) or gate_id not in gate_records:
            errors.append(f"{prefix}: unknown gate_id {gate_id!r}")
        if not HASH_PATTERN.fullmatch(decision_hash):
            errors.append(f"{prefix}: invalid decision_hash")
        if event_type not in ALLOWED_EVENTS:
            errors.append(f"{prefix}: invalid event_type {event_type!r}")

        if declared_previous != previous_hash:
            errors.append(
                f"{prefix}: hash-chain predecessor mismatch; expected {previous_hash!r}"
            )
        computed_hash = compute_event_hash(row)
        if declared_event_hash != computed_hash:
            errors.append(
                f"{prefix}: event_hash mismatch; expected {computed_hash}, got {declared_event_hash}"
            )
        previous_hash = declared_event_hash

        try:
            execution_count = int(row["execution_count"].strip())
        except ValueError:
            execution_count = -1
            errors.append(f"{prefix}: execution_count must be 0 or 1")
        if execution_count not in {0, 1}:
            errors.append(f"{prefix}: execution_count must be 0 or 1")

        for field in required_event_fields:
            if not row[field].strip():
                errors.append(f"{prefix}: {field} is required")

        prior = state_by_handoff.get(handoff_id)
        if prior is None:
            if event_type != "issued":
                errors.append(f"{prefix}: first handoff event must be issued")
            if execution_count != 0:
                errors.append(f"{prefix}: issuance must have execution_count 0")
            if gate_id in issued_gates:
                errors.append(f"{prefix}: gate {gate_id} already issued a handoff")
            issued_gates.add(gate_id)
            decision_key = (gate_id, decision_hash)
            if decision_key in issued_decisions:
                errors.append(f"{prefix}: replay or second issuance for {gate_id} decision")
            issued_decisions.add(decision_key)
            issuance_positions.append((gate_id, event_id, line_number - 1))

            gate_status = gate_records.get(gate_id, {}).get("status")
            if gate_status not in APPROVED_STATUSES:
                errors.append(f"{prefix}: issuance requires an approved gate")
            if gate_hashes.get(gate_id) != decision_hash:
                errors.append(f"{prefix}: issuance decision_hash does not match current gate")

            seen_handoff_ids.add(handoff_id)
            state_by_handoff[handoff_id] = {
                "handoff_id": handoff_id,
                "gate_id": gate_id,
                "decision_hash": decision_hash,
                "status": event_type,
                "execution_count": execution_count,
                "issued_event": event_id,
                "terminal_event": None,
            }
            continue

        if event_type == "issued":
            errors.append(f"{prefix}: terminal or existing handoff cannot be reissued")
        if prior["status"] in TERMINAL_EVENTS:
            errors.append(f"{prefix}: no event may follow terminal state {prior['status']}")
        if gate_id != prior["gate_id"] or decision_hash != prior["decision_hash"]:
            errors.append(f"{prefix}: handoff gate or decision hash changed")
        if event_type == "consumed" and execution_count != 1:
            errors.append(f"{prefix}: consumed event must have execution_count 1")

        prior["status"] = event_type
        prior["execution_count"] = execution_count
        prior["terminal_event"] = event_id

    expected_count = len(rows)
    expected_head_event = rows[-1]["event_id"] if rows else None
    expected_head_hash = rows[-1]["event_hash"].lower() if rows else ""
    if head.get("version") != 1:
        errors.append("Unsupported handoff ledger head version")
    if head.get("event_count") != expected_count:
        errors.append("Handoff ledger event_count does not match anchored head")
    if head.get("head_event_id") != expected_head_event:
        errors.append("Handoff ledger head_event_id mismatch")
    if head.get("head_hash") != expected_head_hash:
        errors.append("Handoff ledger head_hash mismatch")

    seen_checkpoint_ids: set[str] = set()
    trusted_checkpoint_counts: set[int] = set()
    checkpoint_summaries: list[dict[str, object]] = []
    for checkpoint_index, checkpoint in enumerate(checkpoints, start=1):
        prefix = f"trusted-handoff-checkpoints.json:{checkpoint_index}"
        if not isinstance(checkpoint, dict):
            errors.append(f"{prefix}: checkpoint must be an object")
            continue

        checkpoint_id = str(checkpoint.get("checkpoint_id", "")).strip()
        status = str(checkpoint.get("status", "")).strip()
        handoff_id = str(checkpoint.get("handoff_id", "")).strip()
        head_event_id = str(checkpoint.get("head_event_id", "")).strip()
        head_hash = str(checkpoint.get("head_hash", "")).strip().lower()
        terminal_state = str(checkpoint.get("terminal_state", "")).strip()
        event_count = checkpoint.get("event_count")
        decision_owner = str(checkpoint.get("decision_owner", "")).strip()
        signed_at = checkpoint.get("signed_at")
        signature_evidence = checkpoint.get("external_signature_evidence")

        if not CHECKPOINT_ID_PATTERN.fullmatch(checkpoint_id):
            errors.append(f"{prefix}: invalid checkpoint_id {checkpoint_id!r}")
        if checkpoint_id in seen_checkpoint_ids:
            errors.append(f"{prefix}: duplicate checkpoint_id {checkpoint_id}")
        seen_checkpoint_ids.add(checkpoint_id)
        if status not in CHECKPOINT_STATUSES:
            errors.append(f"{prefix}: invalid status {status!r}")
        if not HANDOFF_ID_PATTERN.fullmatch(handoff_id):
            errors.append(f"{prefix}: invalid handoff_id {handoff_id!r}")
        if terminal_state not in TERMINAL_EVENTS:
            errors.append(f"{prefix}: terminal_state must be terminal")
        if not decision_owner:
            errors.append(f"{prefix}: decision_owner is required")
        if not HASH_PATTERN.fullmatch(head_hash):
            errors.append(f"{prefix}: invalid head_hash")

        if status == "pending_human_signature":
            if signed_at not in {None, ""} or signature_evidence not in {None, ""}:
                errors.append(
                    f"{prefix}: pending checkpoint cannot claim signature evidence"
                )
        elif status in {"trusted", "superseded"}:
            if not isinstance(signed_at, str) or not signed_at.strip():
                errors.append(f"{prefix}: {status} checkpoint requires signed_at")
            if not isinstance(signature_evidence, str) or not signature_evidence.strip():
                errors.append(
                    f"{prefix}: {status} checkpoint requires external signature evidence"
                )

        if not isinstance(event_count, int) or isinstance(event_count, bool):
            errors.append(f"{prefix}: event_count must be an integer")
            continue
        if event_count < 1 or event_count > len(rows):
            errors.append(f"{prefix}: event_count is outside the ledger")
            continue

        checkpoint_row = rows[event_count - 1]
        if checkpoint_row["event_id"].strip() != head_event_id:
            errors.append(f"{prefix}: head_event_id does not match ledger checkpoint")
        if checkpoint_row["event_hash"].strip().lower() != head_hash:
            errors.append(f"{prefix}: head_hash does not match ledger checkpoint")
        if checkpoint_row["handoff_id"].strip() != handoff_id:
            errors.append(f"{prefix}: handoff_id does not match checkpoint event")
        if checkpoint_row["event_type"].strip() != terminal_state:
            errors.append(f"{prefix}: terminal_state does not match checkpoint event")

        if status == "trusted":
            trusted_checkpoint_counts.add(event_count)
        checkpoint_summaries.append(
            {
                "checkpoint_id": checkpoint_id,
                "event_count": event_count,
                "status": status,
            }
        )

    for gate_id, event_id, issuance_position in issuance_positions:
        if issuance_position > 1 and issuance_position - 1 not in trusted_checkpoint_counts:
            errors.append(
                f"{event_id}: issuance for {gate_id} requires a trusted checkpoint "
                "for the immediately preceding terminal event"
            )

    if rows and rows[-1]["event_type"].strip() in TERMINAL_EVENTS:
        if not any(
            isinstance(checkpoint, dict)
            and checkpoint.get("event_count") == len(rows)
            for checkpoint in checkpoints
        ):
            errors.append("Current terminal ledger head has no checkpoint record")

    for gate_id, gate_record in gate_records.items():
        if gate_record.get("status") in APPROVED_STATUSES and gate_id not in issued_gates:
            errors.append(f"Approved gate {gate_id} has no handoff issuance event")

    active_by_gate: dict[str, int] = {}
    for state in state_by_handoff.values():
        if state["status"] == "issued":
            gate_id = str(state["gate_id"])
            active_by_gate[gate_id] = active_by_gate.get(gate_id, 0) + 1
    for gate_id, count in active_by_gate.items():
        if count > 1:
            errors.append(f"Multiple active handoffs for {gate_id}")

    return {
        "valid": not errors,
        "errors": errors,
        "event_count": len(rows),
        "head_hash": expected_head_hash,
        "handoffs": list(state_by_handoff.values()),
        "checkpoints": checkpoint_summaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ledger", type=Path, default=Path("research/handoffs.csv"), help="Event CSV"
    )
    parser.add_argument(
        "--decisions", type=Path, default=Path("research/decisions"), help="Gate directory"
    )
    parser.add_argument(
        "--head",
        type=Path,
        default=Path("research/handoff-ledger-head.json"),
        help="Anchored event-ledger head",
    )
    parser.add_argument(
        "--checkpoints",
        type=Path,
        default=Path("research/trusted-handoff-checkpoints.json"),
        help="Human-attested trusted checkpoint records",
    )
    args = parser.parse_args()
    result = validate_handoffs(
        args.ledger.resolve(),
        args.decisions.resolve(),
        args.head.resolve(),
        args.checkpoints.resolve(),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
