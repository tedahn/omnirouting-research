# CONTROL-001 — Deterministic Gate Clerk

- **Type:** Deterministic control, not an LLM advisor
- **Supported gates:** G0-G6
- **Human counterpart:** Named decision owner
- **Artifact:** Validated gate-state update and exactly one bounded handoff

## Purpose

Validate and persist an explicit human decision without interpreting, recommending, or changing it.

## Required checks

- Decision owner identity and eligibility match the gate.
- Accountable-owner conflict declaration is explicit; a conflicted owner is replaced by a named eligible alternate through a superseding record.
- Required distinct-human concurrence and recusal declarations are present.
- Decision is one allowed state and is unambiguous.
- Gate ID, evidence hashes, budget, expiry, source/data boundary, allowed actions, and stop rules are complete and current.
- Conditions, rationale, dissent, reversal evidence, timestamp, and signature are recorded.
- Before a second or later handoff issuance, the immediately preceding terminal event has a human-attested external checkpoint with exact event ID and hash.
- Earlier rejected, revised, expired, and superseded states remain in history.

Run `python3 scripts/validate_gate.py <gate-files>` and `python3 scripts/validate_handoffs.py` before any state-dependent handoff. The validators check structure, decision hashes, single issuance, active-gate eligibility, consumption state, checkpoint-to-ledger correspondence, and trusted-checkpoint sequencing. Human eligibility, signature authenticity, external task-message authenticity, conflicts, and substantive judgment still require human confirmation.

The local chain and checkpoint file are tamper-evident audit artifacts, not tamper-proof storage. Trust comes from the named human repeating the exact checkpoint token in an external decision message; the clerk records that message reference but does not claim a cryptographic signature it cannot verify.

## Failure behavior

If any check fails, make no state change. Return `in_review` or leave `proposed`, name the exact failed field, and request one precise human correction. Silence, agent recommendations, majority votes, and broad prior approval are never valid signatures.

## Successful output

Persist the human-selected state and its external checkpoint attestation. Then append one hash-chained `issued` event with the signed decision hash, advance the local ledger head, and issue exactly one uniquely identified, single-use handoff listing newly allowed work, still-forbidden work, owner, budget, expiry, inputs, validation, and every stop condition. Completion, budget exhaustion, expiry, or any stop trigger appends one terminal event and advances the head; terminal history is never rewritten or reissued. The clerk cannot authorize a later gate.
