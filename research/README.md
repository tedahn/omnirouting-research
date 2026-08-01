# Research state

This directory contains active, reviewed OmniRouting research—not reusable foundry templates.

- `briefs/` frames decision-oriented research before retrieval.
- `profiles/` stores one evidence-grounded record per company or entity.
- `decisions/` stores reviewed decision records; drafts must be labeled.
- `context-packs/` stores bounded, provenance-aware inputs tied to a human gate and consumer prompt.
- `snapshots/` stores dated volatile evidence and refresh triggers.
- `company-landscape.csv`, `methodologies.csv`, `outcomes.csv`, and `future-scenarios.csv` keep entity discovery, mechanisms, evidence, and forecasts separate.
- The remaining CSV ledgers preserve claims, sources, assumptions, evaluations, and protocol changes.
- `NEXT_ACTION-*.md` contains the one currently owned action and its approval boundary.
- `RESEARCH_SPRINT-001.md` defines the first iterative collection, contradiction, reproduction, and refresh loop.
- `briefs/PROFESSIONAL_PROMPT-2026-07-28.md` preserves the execution-ready research specification for this pass.
- `briefs/PROFESSIONAL_PROMPT-continuous-theory-workflow-2026-07-28.md` preserves the specification used to build the continuous workflow.
- `briefs/PROFESSIONAL_PROMPT-research-workflow-batch-2026-07-29.md` preserves the bounded independent discovery and contradiction specification used for pass 2.
- `briefs/PROFESSIONAL_PROMPT-pass-3-consolidation-audit-2026-07-29.md` preserves the execution contract for the bounded pass-3 audit and stop rule.
- `briefs/PROFESSIONAL_PROMPT-conformal-integration-and-saturation-test-2026-07-29.md` preserves the bounded conformal-integration and independent saturation-test contract.
- `briefs/PROFESSIONAL_PROMPT-continue-remaining-work-2026-07-30.md` preserves the governed continuation contract that validates current state and stops at GATE-002 unless the named human explicitly decides.
- `workflows/CONTINUOUS_THEORY_AND_TEST_WORKFLOW.md` defines the bounded scientific and meta-routing loops; it is not an active scheduler.
- `workflows/HUMAN_AI_RESEARCH_PROCESS.md` defines the human decision rights, context contract, prompt contract, separation of duties, and G0-G6 gate ladder governing those loops.
- `workflows/HUMAN_DECISION_AGENT_COUNCIL.md` defines three core AI advisors, an optional blinded-scoring assistant, deterministic gate checks, human concurrence, recusal, escalation, and one-decision routing.
- `agents/` contains reusable advisory role cards and the common authority/output contract; none of the agents can sign a gate or count toward human concurrence.
- `workflows/templates/HUMAN_DECISION_PACKET.md` is the reusable decision interface for options, evidence, dissent, authority delta, human signature, and handoff.
- `../scripts/validate_gate.py` is the deterministic Gate Clerk structure/state validator; human identity, eligibility, conflicts, and judgment remain human checks.
- `handoffs.csv`, `handoff-ledger-head.json`, `trusted-handoff-checkpoints.json`, and `../scripts/validate_handoffs.py` implement an append-only hash-chained lifecycle that enforces unique decision issuance, active-gate eligibility, irreversible terminal states, local-head integrity, and human-attested checkpoints before later issuance.
- `decisions/GATE-002-agora-public-source-integration.md` and `decisions/PACKET-002-agora-integration.md` present the current single human decision; GATE-002 remains proposed.
- `validation/HUMAN_AI_SKILLS-2026-07-29.md` records official static validation and three independent forward scenarios for the governance, context-engineering, and evaluable-prompt skills.
- `validation/HUMAN_DECISION_COUNCIL-2026-07-30.md` records the council topology, deterministic gate and handoff enforcement, six regression cases, independent forward reviews, and remaining human blockers.
- `workflows/VALIDATION-DRY-RUN-2026-07-28.md` records the provisional static stop-path check; it is not a model-run transcript or scientific result.
- `prompts/CONTINUOUS_THEORY_CYCLE_PROMPT.md` runs exactly one resumable cycle per invocation.
- `validation/eval-006/FINAL_REPORT.md` records the transcript-backed synthetic controller checks, hashes, regression, and pending human-review gate.
- `../scripts/validate_eval006.py` deterministically verifies EVAL-006 hashes, metrics, cases, and scientific-ledger isolation. Its frozen ledger hashes are expected to fail after later governed research edits until EVAL-006 is deliberately refreshed.
- `snapshots/2026-07-28-routing-company-source-map.md` is the first dated company, technique, outcome, counterevidence, and transaction-status map.
- `snapshots/2026-07-29-independent-discovery-and-contradiction-pass.md` records the material pass-2 expansion, status reconciliation, saturation failure, and bounded pass-3 action.
- `snapshots/2026-07-29-pass-3-consolidation-audit.md` records the pass-3 corrections, routing-layer map, eight-entity priority queue, and material no-addition failure that keeps Stage 1 open.
- `snapshots/2026-07-29-conformal-integration-and-saturation-test.md` records MTH-017, its exact guarantee limits and benchmark result, and the GAR material-addition stop that resets saturation testing.
- `snapshots/2026-07-29-gar-integration-and-auction-stop.md` records MTH-018, modeled-carbon boundaries, GAR's exact offline result, and the Agora material-addition stop from post-GAR formulation 001.

AI-generated material remains provisional until a reviewer verifies its evidence and promotes it into the relevant ledger or decision record.
