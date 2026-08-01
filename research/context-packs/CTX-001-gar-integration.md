# CTX-001 — GAR evidence integration

- **Version:** 1.0
- **Built at:** 2026-07-29
- **Owner:** Workspace requester acting as research lead
- **Consumer:** Bounded GAR evidence-integration prompt
- **Supported gate:** `../decisions/GATE-001-gar-public-source-integration.md`
- **Canonical state:** `../../CURRENT_STATE.md`
- **Context budget:** Decision core plus exact primary excerpts; six primary-source opens or 60 minutes
- **Refresh trigger:** Material GAR revision, new replication, source conflict, model/data change, or gate expiry

## Decision and success criteria

Decide how GAR changes the OmniRouting taxonomy and evidence map. Extract exact source-backed method and outcome records, keep carbon distinct from energy and money, and preserve assumptions and limitations. Success requires valid ledgers and an explicit Stage-1 gate result.

## Authorized actions

- Inspect public primary artifacts.
- Add or correct source-backed research rows and a dated snapshot.
- Run one no-addition formulation only after GAR integration and only if no earlier stop fires.

## Forbidden actions

No private data, vendor contact, paid access, unreviewed code execution, experiment, scheduler, theory promotion, EVAL-006 rebaseline, production recommendation, or deployment.

## Current state

- Stage 1 remains open.
- Ledgers contain 29 candidates, 65 sources, 34 claims, 17 methods, and 24 outcomes.
- MTH-007 covers global cost/quality/capacity allocation; MTH-008 and OUT-014 cover online SLA-aware allocation and energy measured in megajoules.
- No structured record yet covers time-varying grid carbon intensity, per-request CO2, accuracy plus p95-latency constraints, or a rolling carbon budget.

## Evidence index

| ID | State | Source/version | Exact location | Supports or contradicts | Freshness |
|---|---|---|---|---|---|
| CTX-E01 | observed | `../../CURRENT_STATE.md` | Current gate and material unknowns | Scope and blockers | 2026-07-29 |
| CTX-E02 | observed | `../NEXT_ACTION-001.md` | Do and stop rule | Authorized next action | 2026-07-29 |
| CTX-E03 | observed | `../snapshots/2026-07-29-conformal-integration-and-saturation-test.md` | Bottom line and gate decision | Why GAR is material | 2026-07-29 |
| CTX-E04 | reported candidate | `https://arxiv.org/abs/2605.11603` v1 | Abstract; exact PDF locations pending | GAR mechanism and carbon endpoint | 2026-05-12 |
| CTX-E05 | source_backed | `../methodologies.csv` MTH-007 and MTH-008 | Full rows | Nearest constrained-allocation families | 2026-07-29 |
| CTX-E06 | source_backed | `../outcomes.csv` OUT-014 | Full row | Energy, not carbon, comparator | 2025-10-23 |

## Contradiction register

| Claim | Supporting evidence | Counterevidence | Disposition |
|---|---|---|---|
| GAR adds a material routing category | Primary abstract describes grid-carbon signals, CO2 objective, SLO constraints, and rolling budget | MTH-007 and MTH-008 already contain constrained allocation | Resolve by exact mechanism comparison; carbon outcome remains distinct unless primary evidence says otherwise |
| Carbon savings imply monetary or energy savings | None admitted | OUT-014 shows energy units differ; prices and grid mix vary | Prohibited inference |
| GAR is production-ready | No customer-grade evidence admitted | Current state records sparse production validation | Unsupported |

## Material unknowns

- Exact GAR algorithm, objective, estimator equations, carbon-intensity source, constraint handling, tables, datasets, models, sample counts, numerical results, ablations, limitations, and repository pin.
- Whether MTH-007 should be extended or a new composable carbon-aware family is required.
- Whether incentive-market and user-choice leads remain material after GAR integration.

## Excluded context

| Item | Reason | Reconsider when |
|---|---|---|
| Private workload traces | Not authorized | Safety/privacy and G4 approvals exist |
| Future experiment design details | Stage 1 only | G2 closes and G3 opens |
| Promotional secondary summaries | Primary evidence required | Only for discovery if primary remains identifiable |
| EVAL-006 hash refresh | Frozen validation integrity | Explicit human rebaseline decision |

## Required output

One dated integration snapshot; source-backed source, claim, methodology, and outcome deltas; updated current gate and next action; exact source-open count; and a stopped or provisional status.

## Validation

Run the workspace validator, CSV and cross-reference checks, `git diff --check`, and EVAL-006 without changing its manifest. Require exact primary locations for central claims.

## Stop and fallback rules

Stop on material novelty, inaccessible central evidence, budget exhaustion, source conflict that blocks classification, private-data need, or validation failure. If stopped, persist the candidate and exactly one bounded next action without synthesis promotion.

## Handoff

Preserve gate, source versions, method/outcome distinctions, contradictions, unknowns, budget, stop result, and next owner before narrative history.
