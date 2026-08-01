#!/usr/bin/env python3
"""Regression tests for append-only, single-use handoff enforcement."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_handoffs import (  # noqa: E402
    EXPECTED_HEADERS,
    compute_event_hash,
    validate_handoffs,
)


class HandoffValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = ROOT / "research" / "handoffs.csv"
        self.head = ROOT / "research" / "handoff-ledger-head.json"
        self.checkpoints = ROOT / "research" / "trusted-handoff-checkpoints.json"
        self.decisions = ROOT / "research" / "decisions"
        with self.ledger.open(newline="", encoding="utf-8") as handle:
            self.rows = [dict(row) for row in csv.DictReader(handle)]
        self.current_head = json.loads(self.head.read_text(encoding="utf-8"))
        self.current_checkpoints = json.loads(
            self.checkpoints.read_text(encoding="utf-8")
        )

    def append_event(
        self, rows: list[dict[str, str]], overrides: dict[str, str]
    ) -> list[dict[str, str]]:
        row = dict(rows[0])
        row.update(overrides)
        row["previous_event_hash"] = rows[-1]["event_hash"] if rows else ""
        row["event_hash"] = compute_event_hash(row)
        return [*rows, row]

    def write_fixture(
        self,
        directory: Path,
        rows: list[dict[str, str]],
        head: dict[str, object] | None = None,
        checkpoints: dict[str, object] | None = None,
    ) -> tuple[Path, Path, Path]:
        ledger = directory / "handoffs.csv"
        with ledger.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=EXPECTED_HEADERS)
            writer.writeheader()
            writer.writerows(rows)
        if head is None:
            head = {
                "version": 1,
                "event_count": len(rows),
                "head_event_id": rows[-1]["event_id"] if rows else None,
                "head_hash": rows[-1]["event_hash"] if rows else "",
            }
        head_path = directory / "handoff-ledger-head.json"
        head_path.write_text(json.dumps(head), encoding="utf-8")
        checkpoint_path = directory / "trusted-handoff-checkpoints.json"
        checkpoint_path.write_text(
            json.dumps(
                self.current_checkpoints if checkpoints is None else checkpoints
            ),
            encoding="utf-8",
        )
        return ledger, head_path, checkpoint_path

    def validate_fixture(
        self,
        rows: list[dict[str, str]],
        head: dict[str, object] | None = None,
        checkpoints: dict[str, object] | None = None,
    ) -> dict[str, object]:
        with tempfile.TemporaryDirectory(prefix="omnirouting-handoff-test-") as tmp:
            ledger, head_path, checkpoint_path = self.write_fixture(
                Path(tmp), rows, head, checkpoints
            )
            return validate_handoffs(
                ledger, self.decisions, head_path, checkpoint_path
            )

    def test_current_ledger_is_valid(self) -> None:
        result = validate_handoffs(
            self.ledger, self.decisions, self.head, self.checkpoints
        )
        self.assertTrue(result["valid"], result["errors"])

    def test_duplicate_decision_issuance_is_rejected_as_replay(self) -> None:
        replay = self.append_event(
            self.rows,
            {
                "event_id": "EVENT-999",
                "handoff_id": "HANDOFF-999",
                "event_type": "issued",
                "execution_count": "0",
                "reason": "Replay test",
                "notes": "Negative fixture",
            },
        )
        result = self.validate_fixture(replay)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "already issued" in error or "replay or second issuance" in error
                for error in result["errors"]
            ),
            result["errors"],
        )

    def test_proposed_gate_cannot_issue_handoff(self) -> None:
        gate = self.decisions / "GATE-002-agora-public-source-integration.md"
        unauthorized = self.append_event(
            self.rows,
            {
                "event_id": "EVENT-003",
                "handoff_id": "HANDOFF-002",
                "gate_id": "GATE-002",
                "decision_hash": hashlib.sha256(gate.read_bytes()).hexdigest(),
                "event_type": "issued",
                "execution_count": "0",
                "authorized_action": "Agora integration",
                "budget": "Four primary-source opens or 60 minutes",
                "expires_at": "2026-08-06 or stop trigger",
                "stop_conditions": "Any GATE-002 stop condition",
                "required_output": "Provisional records and snapshot",
                "validation": "validate_workspace.py; validate_handoffs.py",
                "reason": "Unauthorized issuance test",
                "notes": "Negative fixture",
            },
        )
        result = self.validate_fixture(unauthorized)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("issuance requires an approved gate" in error for error in result["errors"]),
            result["errors"],
        )

    def test_terminal_handoff_cannot_transition_to_issued(self) -> None:
        reactivated = self.append_event(
            self.rows,
            {
                "event_id": "EVENT-003",
                "handoff_id": "HANDOFF-001",
                "event_type": "issued",
                "execution_count": "0",
                "reason": "Reactivation test",
                "notes": "Negative fixture",
            },
        )
        result = self.validate_fixture(reactivated)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("cannot be reissued" in error for error in result["errors"]),
            result["errors"],
        )

    def test_terminal_event_deletion_breaks_anchored_head(self) -> None:
        truncated = self.rows[:1]
        rewritten_local_head = {
            "version": 1,
            "event_count": 1,
            "head_event_id": truncated[-1]["event_id"],
            "head_hash": truncated[-1]["event_hash"],
        }
        result = self.validate_fixture(truncated, rewritten_local_head)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "checkpoint" in error or "outside the ledger" in error
                for error in result["errors"]
            ),
            result["errors"],
        )

    def test_second_issuance_requires_trusted_prior_checkpoint(self) -> None:
        second_issuance = self.append_event(
            self.rows,
            {
                "event_id": "EVENT-003",
                "handoff_id": "HANDOFF-002",
                "event_type": "issued",
                "execution_count": "0",
                "reason": "Checkpoint enforcement test",
                "notes": "Negative fixture",
            },
        )
        result = self.validate_fixture(second_issuance)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("requires a trusted checkpoint" in error for error in result["errors"]),
            result["errors"],
        )


if __name__ == "__main__":
    unittest.main()
