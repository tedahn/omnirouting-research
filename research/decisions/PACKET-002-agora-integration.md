# PACKET-002 — Agora integration scope decision

- **Gate:** `GATE-002` / G0 Scope
- **Gate status:** proposed
- **Decision owner:** Workspace requester acting as research lead
- **Prepared by:** Initial advisory council draft; not independent review
- **Evidence snapshot:** `../snapshots/2026-07-29-gar-integration-and-auction-stop.md` SHA-256 `1a8e03b102b8eda71bcf65f3c332a593e2e6214d4aeb9cb7f03ec677d3fa0ec6`
- **Prepared at:** 2026-07-30
- **Expires at:** 2026-08-06, completion, budget exhaustion, any stop trigger, or material snapshot change—whichever occurs first

## One decision requested

Should `GATE-002` authorize one public-source-only Agora evidence-integration delta capped at four primary-source opens or 60 minutes?

## Options and consequences

| Option | Authority granted | What remains forbidden | Consequence |
|---|---|---|---|
| Approve | Exact GATE-002 in-scope authority under its budget, expiry, and stop rules | G1/G2 acceptance, later candidates, code execution, experiments, Stage 2, production | Research can execute the bounded delta without additional discretionary conditions |
| Approve with conditions | Agora extraction and provisional record drafting within the stated budget | G1/G2 acceptance, later candidates, code execution, experiments, Stage 2, production | Research can verify the disputed mechanism and return to G1 |
| Revise | None until resubmitted | All proposed work | Owner changes budget, scope, roles, or conditions |
| Reject | None | All proposed work | Agora remains excluded with the recorded rationale |
| Defer | None until a named trigger | All proposed work | Wait for a new version, code, reviewer, or other stated event |
| Expire | None | All proposed work | Open a fresh gate if the work is still needed |

## Advisory contributions

| Advisor | Finding | Human counterpart | Review status |
|---|---|---|---|
| Gate Navigator | This is one G0 scope decision; later evidence and synthesis decisions remain separate | Research lead | Advisory |
| Evidence and Methods Challenger | Not invoked for G0; exact payment/proof basis, denominators, cost accounting, strategic-agent tests, and implementation are queued for the G1/G2 challenge | Evidence and methodology reviewers | Deferred; humans unassigned for later G1/G2 |
| Boundary Sentinel | Public-only extraction is reversible if capped; private data, spend, code execution, later candidates, and promotion remain forbidden | Research lead for this G0 | Advisory |
| Gate Clerk | Gate remains proposed until an explicit command passes deterministic identity, eligibility, hash, budget, expiry, signature, and prior-terminal-checkpoint checks | Decision owner | Awaiting decision and checkpoint attestation |

## Advisory recommendation

**Advisory only:** `approve_with_conditions` using the budget and restrictions in GATE-002. Confidence is moderate because the operation is reversible and bounded, but the substantive incentive-compatibility claim is unresolved. The strongest countercase is that Agora may be calibrated utility routing described with auction language rather than a formally incentive-compatible economic mechanism.

## Evidence and contradiction register

| Claim | State | Exact provenance | Counterevidence or gap | Freshness | Owner | Decision impact |
|---|---|---|---|---|---|---|
| Agora uses auction-framed calibrated step allocation | source_backed | arXiv `2607.09600v1`, Sections 1 and 3; prior snapshot | Independent replication absent | Paper submitted 2026-07-10; refresh at gate expiry or new version | Bounded researcher | Supports bounded integration |
| Agora is incentive-compatible | reported | arXiv v1 abstract and framing | No exact payment rule, theorem, or strategic-agent test located in the bounded prior read | Refresh during delta | Evidence reviewer unassigned | Must not be accepted without extraction and G1 review |
| Agora is distinct from current families | proposed | Prior snapshot comparison with MTH-009, MTH-014, and MTH-016 | Full method extraction pending | Reassess after delta | Methodology reviewer unassigned | Justifies investigation, not taxonomy promotion |
| Public-source review is low consequence | inferred | GATE-002 source/data boundary and prohibited-action list | Retrieval can still expose conflicting or stale evidence | Expires 2026-08-06 | Boundary Sentinel advisory | Supports capped, stoppable work |

## Unresolved fields

| Field | Current value | Blocking? | Owner | Resolution evidence |
|---|---|---|---|---|
| Payment/transfer rule and formal incentive-compatibility basis | unresolved | Blocks accepting that claim at G1/G2 | Evidence reviewer unassigned | Exact equation, theorem, proof, assumptions, or explicit absence |
| Strategic-agent, collusion, or gaming evaluation | unresolved | Blocks robustness claims | Methodology reviewer unassigned | Primary experiment and exact result locations or explicit absence |
| Implementation repository and pin | unresolved | Blocks reproducibility claim | Bounded researcher | Official repository URL and commit, or documented no-artifact result |
| Cost accounting and bid-call overhead | unresolved | Blocks normalized outcome record | Bounded researcher | Exact price, token/call, denominator, and overhead locations |
| Independent replication | none located | Does not block G0; blocks stronger promotion/adoption claims | Future independent evaluator | Reproducible external result |
| Human evidence and methodology reviewers | unassigned | Blocks G1 and G2, not this low-risk G0 | Research lead | Named eligible humans with conflict declarations |

## Acceptance and failure

- **Acceptance:** Every GATE-002 acceptance criterion is satisfied or explicitly unresolved; provisional records preserve exact versions, locations, units, denominators, counterevidence, and absence claims.
- **Failure:** Central allocation evidence is inaccessible or contradictory, the public-only boundary is crossed, the four-open/60-minute budget or expiry is reached, scope expands beyond Agora, or required validation fails.
- **Decision effect:** G0 approval authorizes collection and drafting only. It does not resolve any field above or pass G1/G2.

## Separation of duties

| Function | Named human | Advisory/control role | Status |
|---|---|---|---|
| G0 accountable decision | Workspace requester acting as research lead; conflict declaration pending | Gate Navigator and Boundary Sentinel | A conflict requires recusal and a named eligible alternate |
| G1 evidence admission | Unassigned | Evidence and Methods Challenger | Blocks G1 only |
| G2 method/synthesis acceptance | Unassigned | Evidence and Methods Challenger | Blocks G2 only |
| Gate-state recording | Workspace requester signature required | Deterministic Gate Clerk | No state change until signature validates |
| Independent evaluation | Not applicable at G0 | Blind Evaluation Assistant not invoked | No independence claim |

## Authority delta if approved

- **Newly authorized:** Public primary-source retrieval, extraction, comparison, provisional ledger drafting, deterministic validation, and advisory challenge for Agora only.
- **Still forbidden:** Evidence admission, synthesis acceptance, later discovery, experiments, code execution, profiles, scheduling, theory promotion, production, publication, and EVAL-006 rebaselining.
- **Budget:** Four primary-source opens or 60 minutes, whichever comes first.
- **Expiry:** 2026-08-06, completion, budget exhaustion, any stop trigger, or material input change—whichever occurs first.
- **Consumption:** The Gate Clerk issues one uniquely identified handoff; it is consumed on completion or stop and cannot be reused.
- **Prior-state checkpoint:** `CHECKPOINT-001 EVENT-002 7b76dec742ec39acb454a37298b0b0fe7e589c9031cfaa966505f1567bc308ae` must be attested in the approval message and recorded as trusted before issuance.
- **First stop:** Central mechanism evidence is inaccessible, contradictory, outside the public boundary, or materially expands scope.

## Human decision command

The named owner may reply with exactly one of:

- `APPROVE GATE-002 WITH CONDITIONS; CONFLICT: NONE; TRUST CHECKPOINT-001 EVENT-002 7b76dec742ec39acb454a37298b0b0fe7e589c9031cfaa966505f1567bc308ae`
- `APPROVE GATE-002; CONFLICT: NONE; TRUST CHECKPOINT-001 EVENT-002 7b76dec742ec39acb454a37298b0b0fe7e589c9031cfaa966505f1567bc308ae`
- `REVISE GATE-002: <requested change>`
- `REJECT GATE-002: <rationale>`
- `DEFER GATE-002 UNTIL <trigger>`

Silence or a general request to continue does not change gate status.

## Human decision audit

- **Decision:** null
- **Conditions or requested revision:** null
- **Rationale and dissent:** Advisory recommendation and unresolved fields above; human rationale pending
- **Decision-maker identity:** Workspace requester acting as research lead; signature pending
- **Conflict declaration / eligible alternate:** pending / unassigned
- **Decided at:** null
- **Approval decision hash:** null
- **Trusted checkpoint / external signature evidence:** CHECKPOINT-001 pending / null
- **Handoff ID / status:** null / unissued
- **Issued at / closed at / execution count:** null / null / 0
- **Reversal evidence:** New Agora version, formal proof, repository, strategic-agent evidence, materially different cost result, or changed canonical snapshot

## Handoff

Await the explicit human command. After it is recorded, preserve its task-message reference as external signature evidence, mark `CHECKPOINT-001` trusted, hash the signed gate, append exactly one hash-chained `issued` event to `../handoffs.csv`, and advance `../handoff-ledger-head.json`. `python3 scripts/validate_handoffs.py` must reject a second issuance, gate/hash replay, post-terminal event, broken chain, local-head rewrite, checkpoint mismatch, or issuance without an immediately preceding trusted checkpoint. Only then issue the bounded next action.
