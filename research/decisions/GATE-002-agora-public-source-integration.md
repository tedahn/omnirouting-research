# GATE-002 — Agora public-source integration

- **Gate:** G0 Scope
- **Status:** proposed
- **Decision owner:** Workspace requester acting as research lead
- **Requested by:** Gate Navigator advisory draft
- **Opened at:** 2026-07-30
- **Decided at:** null
- **Expires at:** 2026-08-06, completion of one delta, budget exhaustion, any stop trigger, or material evidence-snapshot change—whichever occurs first
- **Supersedes:** null
- **Evidence snapshot:** `../snapshots/2026-07-29-gar-integration-and-auction-stop.md` SHA-256 `1a8e03b102b8eda71bcf65f3c332a593e2e6214d4aeb9cb7f03ec677d3fa0ec6`

## Decision requested

Approve, approve with conditions, revise, reject, or defer **one bounded public-source Agora evidence-integration delta**.

This decision does not admit evidence at G1, accept a synthesis at G2, authorize an experiment, restart saturation testing, begin profiles, or grant any later-gate authority.

## Why now

Post-GAR formulation 001 stopped after Agora exposed a potentially distinct auction-framed, calibrated reasoning-step allocation mechanism. Stage 1 cannot resume its two-formulation saturation test until Agora is either integrated, rejected with evidence, or explicitly deferred.

## In scope

- Inspect Agora arXiv `2607.09600v1` and any directly linked official repository or appendix.
- Verify the allocation objective, bid construction, calibration loop, cost term, any payment or transfer rule, and the exact basis for the phrase `incentive-compatible`.
- Extract benchmark denominators, model pools, baselines, uncertainty, token/call overhead, monetary-cost accounting, and negative ablations.
- Compare the mechanism with MTH-009, MTH-014, and MTH-016.
- Draft provisional source, claim, method, outcome, contradiction, and snapshot records.
- Run deterministic workspace validation and an adversarial advisory challenge; this does not satisfy independent human review.

## Out of scope

- Private or paid data, author/vendor contact, code execution, new model calls, experiments, profiles, rankings, scheduler activation, theory promotion, Stage 2 transition, production action, external publication, or EVAL-006 rebaselining.
- Opening or adjudicating later discovery candidates after an Agora materiality or evidence-boundary stop.
- Treating the paper's `incentive-compatible` wording as an accepted formal guarantee without exact supporting evidence.

## Roles

- **Responsible worker:** Codex as bounded public-source researcher.
- **Accountable human:** Workspace requester acting as research lead.
- **Accountable-owner conflict declaration:** Pending explicit human attestation; a material research, vendor, or financial conflict requires recusal.
- **Named eligible alternate:** Unassigned; required only if the accountable owner declares a conflict.
- **AI advisors for this G0:** Gate Navigator and Boundary Sentinel.
- **Deterministic control:** Gate Clerk after an explicit human response.
- **Deferred advisory role:** Evidence and Methods Challenger at G1/G2, after the delta produces reviewable evidence.
- **Human evidence reviewer:** Unassigned; required with the Evidence and Methods Challenger before G1 admission.
- **Human methodology reviewer:** Unassigned; required with the Evidence and Methods Challenger before G2 acceptance.
- **Not invoked:** Blind Evaluation Assistant, experiment owner, holdout custodian, independent evaluator, and adoption owner because no G3-G6 authority is requested.

## Evidence

- **Observed:** Current state SHA-256 `051b94222bc7067c238f9e4047d3734370ec3b00461b8f3f0330a25b19e611aa` records Stage 1 open, the advisory council, and Agora pending bounded integration.
- **Observed:** `NEXT_ACTION-001.md` SHA-256 `2a845c3c6aaef8c79139f78b241e390f852488e59e7986ec561c6b25f0b38ac9` requires an explicit GATE-002 decision before work begins.
- **Source-backed:** Agora v1 describes planning, hierarchical competence calibration, auction-framed step allocation, execution, composition, and evaluator-driven refinement across five offline benchmarks.
- **Reported:** The abstract calls the mechanism incentive-compatible.
- **Unresolved:** Exact payment/transfer rule, theorem and assumptions, strategic-agent or gaming evaluation, full cost accounting, implementation pin, scale behavior, and independent replication.
- **Contradiction-sensitive:** An auction label and calibrated utility maximization do not by themselves establish economic incentive compatibility.

## Acceptance criteria

- The exact allocation, utility, bid, cost, payment/transfer, and calibration rules are cited or their absence is explicit.
- Any theorem, proposition, proof, or strategic-behavior test supporting incentive compatibility is identified with assumptions; otherwise the claim remains `reported` or `unresolved`.
- All five benchmark settings preserve model pools, samples, baselines, metrics, uncertainty, and overhead without merging incompatible outcomes.
- Code/data artifacts are located and pinned or explicitly recorded as unresolved; code is not executed.
- Taxonomy comparison shows whether a new family is required and states falsifiers.
- Only source-backed provisional records are drafted; G1/G2 human acceptance remains separate.
- `python3 scripts/validate_workspace.py` and `git diff --check` pass.
- The accountable human records `CONFLICT: NONE` or declares a conflict and names an eligible alternate before approval is valid.
- The same explicit approval attests `CHECKPOINT-001`, `EVENT-002`, and head hash `7b76dec742ec39acb454a37298b0b0fe7e589c9031cfaa966505f1567bc308ae`; the Gate Clerk records that task-message reference before any new handoff issuance.

## Stop conditions

- Four primary-source opens, 60 minutes, or 2026-08-06 is reached.
- A private, paid, restricted, or contact-dependent boundary is encountered.
- Exact evidence needed for the central mechanism is contradictory or inaccessible.
- A material mechanism or outcome outside the approved Agora delta appears.
- Canonical hashes change materially before execution.
- The single authorized delta completes; the handoff is consumed and cannot be reused.

## Decision

- **Status:** proposed; no human decision has been recorded.
- **Advisory recommendation:** `approve_with_conditions` because the work is reversible, public-source-only, and tightly bounded.
- **Recommended conditions:** enforce the four-open/60-minute cap; do not execute code; do not accept incentive compatibility without exact support; stop before later candidates; keep G1 and G2 separate.
- **Dissent:** No independent human evidence or methodology reviewer has reviewed the packet.

## Reversal evidence

Reopen or revise the scope if Agora publishes a new version, repository, erratum, formal proof, strategic-agent evaluation, materially different cost result, or if current source hashes change.

## Handoff

No new authority exists while status is `proposed`, and no approval is valid without both the accountable-owner conflict declaration and the exact `CHECKPOINT-001` attestation. No GATE-002 issuance event exists in `../handoffs.csv`; the Gate Clerk must first record the external human attestation in `../trusted-handoff-checkpoints.json`, then append one unique hash-chained `issued` event from the signed decision hash and update `../handoff-ledger-head.json` before work can begin.

If an eligible named human approves with a conflict declaration and the exact checkpoint token, the Gate Clerk records the external task-message evidence, marks `CHECKPOINT-001` trusted, computes the signed gate hash, appends one unique hash-chained `issued` event to `../handoffs.csv`, and advances `../handoff-ledger-head.json` before issuing the handoff to the bounded public-source researcher. Only the `In scope` actions are authorized; every `Out of scope` action remains forbidden. The budget is four primary-source opens or 60 minutes. Authority expires on 2026-08-06, completion, budget exhaustion, any stop trigger, or material snapshot change—whichever occurs first—and cannot be reused. Required output is a provisional source/claim/method/outcome delta, contradiction record, and dated snapshot that pass `python3 scripts/validate_workspace.py`, `python3 scripts/validate_gate.py`, `python3 scripts/validate_handoffs.py`, and `git diff --check`. Completion or stop appends a terminal `consumed`, `expired`, or `revoked` event with execution count and advances the anchored head; terminal history is never rewritten. The next human gate after completion is G1 evidence admission.
