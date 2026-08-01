# Human Decision Agent Council validation — 2026-07-30

- **Scope:** Introduce bounded AI advisory roles and deterministic controls that move human research decisions through G0-G6 without transferring decision authority to an LLM.
- **Status:** Validated as an advisory workflow; GATE-002 remains `proposed` and grants no research authority.
- **Prompt specification:** `../briefs/PROFESSIONAL_PROMPT-human-decision-agent-council-2026-07-30.md`
- **Governance basis:** `../workflows/HUMAN_AI_RESEARCH_PROCESS.md` and the `govern-human-ai-research` skill contract.

## Implemented topology

| Component | Type | Decision right |
|---|---|---|
| Gate Navigator | AI advisor | None |
| Evidence and Methods Challenger | AI advisor for G1-G5 | None |
| Boundary Sentinel | AI advisor | None |
| Blind Evaluation Assistant | Optional G5 calculation support | None; never establishes independence |
| Gate Clerk | Deterministic control | None; records explicit eligible-human decisions only |
| Named human owner and required distinct reviewer | Human | Gate-specific accountability and concurrence |

The current Agora G0 invokes only Gate Navigator and Boundary Sentinel. Evidence and Methods Challenger is deferred to G1/G2, and Blind Evaluation Assistant is not invoked.

## Deterministic enforcement

- `../../scripts/validate_gate.py` validates gate structure, state, owner, timestamp, evidence snapshot path, and declared SHA-256.
- `../../scripts/validate_handoffs.py` validates the global event hash chain, current local head, gate decision hash, unique issuance, terminal-state irreversibility, and prior-terminal checkpoint sequencing.
- `../trusted-handoff-checkpoints.json` records the consumed GATE-001 terminal event. It is pending human attestation and therefore cannot support a later issuance.
- A second or later handoff requires a trusted checkpoint for the immediately preceding terminal event. Local artifacts are described as tamper-evident, not tamper-proof; external human decision evidence remains a human authenticity check.

## Test evidence

`python3 -m unittest -v scripts/test_validate_handoffs.py` passed six cases:

1. current ledger validity;
2. duplicate decision issuance rejection;
3. proposed-gate issuance rejection;
4. terminal handoff reactivation rejection;
5. terminal-event truncation plus recomputed local-head rejection; and
6. later issuance without a trusted prior checkpoint rejection.

`python3 scripts/validate_workspace.py` passed with the checkpoint registry included in required workspace state. `git diff --check` passed.

## Independent forward reviews

- **Prompt review:** A G0/G1 role-routing defect was corrected; final result `PASS`.
- **Context review:** Stale hashes, non-resolving evidence paths, independence wording, incomplete packet fields, and option/handoff inconsistencies were corrected; final result `PASS`.
- **Governance review:** Role/quorum ambiguity, owner recusal, single-use enforcement, mutable-state reactivation, and co-mutable-head concerns were corrected through explicit human concurrence, append-only events, regression tests, and checkpoint attestation; final result `PASS`.

## Known limits and blockers

- Advisory roles are prompt contracts, not independent people or persistent autonomous workers.
- Same-model or same-organization critique never counts as independent human review.
- Human evidence and methodology reviewers remain unassigned, so G1 and G2 cannot pass.
- `CHECKPOINT-001` remains `pending_human_signature`; GATE-002 cannot issue a handoff until the named human explicitly attests its event ID and hash.
- No source collection, experiment, theory promotion, scheduling, publication, or production action was authorized by this implementation.

## Current human decision

The recommended eligible-owner response is preserved exactly in `../decisions/PACKET-002-agora-integration.md`. Until that explicit response is received, GATE-002 remains `proposed` and execution remains stopped.
