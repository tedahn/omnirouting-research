# Validation dry run: continuous theory-and-test workflow

- **Cycle ID:** `DRY-001`
- **As of:** 2026-07-28 America/Chicago
- **Mode:** Theory-to-preregistration dry run
- **Evidence status:** Synthetic workflow validation only; no new empirical evidence
- **Result:** Provisional static protocol check — the written controller reaches the authorization gate and stops without inventing a run; no ChatGPT execution transcript or human approval is claimed

## Input checkpoint

| Field | Dry-run value | Gate |
|---|---|---|
| Decision | Determine whether session-aware routing merits a controlled reproduction | Present |
| Owner | Research lead role; identity unresolved | Blocks execution |
| Target workload | Long-horizon tool-using tasks; exact benchmark unresolved | Blocks execution |
| Model/provider pool | Unresolved | Blocks execution |
| Data boundary | Public evidence only | Allows design, not private/live testing |
| Holdout custodian | Unresolved | Blocks confirmation testing |
| Tools | Document drafting only | Blocks execution |
| Token/dollar/time budget | Unresolved | Blocks execution |
| Independent evaluator | Unresolved | Blocks promotion |

## Synthetic tension

Per-call routing may select the locally strongest model while degrading end-to-end agent performance through context discontinuity, cache misses, inconsistent tool behavior, and retry overhead. Existing workspace evidence makes this plausible but does not establish the causal effect or its boundary.

## Provisional theory card

- **ID:** `HYP-DRY-001` — validation-only; not added to the active hypothesis ledger.
- **Claim:** For long-horizon tool tasks, a session-aware sticky router with explicit escalation will improve task success per total cost over independently routing every call after cache, retry, and failure-recovery costs are included.
- **Mechanism:** Maintaining execution continuity preserves context locality, cache reuse, tool conventions, and error-recovery state; escalation captures tasks that exceed the pinned model's capability.
- **Predicted interaction:** The advantage should increase with context length, tool-state dependence, and provider cache discounts, but shrink when task phases require sharply different capabilities.
- **Scope:** Multi-step tool tasks; not one-turn classification or simple fallback routing.
- **Strongest rival:** Capability-vector per-call routing wins because phase-specific specialization outweighs continuity costs.
- **Hard falsifier:** On untouched long-horizon tasks, an adequately powered equivalence/non-inferiority analysis excludes the preregistered meaningful improvement, or the candidate produces material harm/opposite effect in task success per total cost, catastrophic error, policy, or tail latency. A merely non-significant result is inconclusive.
- **Boundary conditions:** Cache semantics, provider failure rates, escalation policy, model pool, tool interface, and task horizon.
- **Novelty label:** Known mechanism with a potentially new boundary or decisive test; field novelty not established.
- **Decision value:** A positive result prioritizes session/SLA-aware routing experiments; a negative result redirects effort toward per-call capability selection.

## Preregistration draft

- **H0:** Session-aware sticky routing does not improve the chosen primary utility beyond the minimum meaningful effect versus per-call routing.
- **H1:** It does improve that utility while meeting all hard guardrails.
- **Candidate:** Sticky session assignment with a declared escalation policy.
- **Controls:** Static best model, cheapest model, random eligible model, deterministic rules, learned per-call selector, and oracle where calculable.
- **Splits:** Exploration set; untouched confirmation set; temporal or model-pool-change replication set.
- **Candidate metrics:** Task success, cost per successful task, p50/p95/p99 latency, routing regret, fallback/escalation rate, cache effects, catastrophic error, policy violations, and model-churn resilience.
- **Missing preregistration fields:** Exact workload, model pool, primary metric, minimum meaningful effect, sample size/power, seeds, budget, evaluator, and replication owner.
- **Execution decision:** `STOPPED_PRE_EXECUTION`.

## Meta-routing dry run

| Subtask | Proposed route | Independence note |
|---|---|---|
| Schema and invariant checks | Deterministic code | Appropriate once fixtures exist |
| Evidence extraction | Lowest-cost model that passes extraction evals | Requires citation entailment checks |
| Theory generation | Strong reasoning model | Generates conjectures only |
| Prior-art challenge | Separate context/model family plus primary-source search | Not available in this dry run |
| Final grading | Deterministic metrics plus independent evaluator | Not available in this dry run |

No model-quality, cost, or latency measurements were fabricated.

## Ledger deltas

- `sources.csv`, `claims.csv`, `outcomes.csv`, and `assumptions-forecasts.csv`: none; the dry run is not evidence.
- `eval-cases.csv`: provisional static protocol cases `EVAL-003` through `EVAL-005` record the required controls; `EVAL-006` reserves the first transcript-backed positive-path and bypass-resistance run.
- `change-log.csv`: `CHANGE-003` records the controller as a proposed, inactive protocol change.

## Stop and resume

- **Stop reason:** Owner identity, target workload, model pool, holdout custodian, evaluator, and execution budgets are unresolved.
- **Next action:** The research lead chooses the target workload and sets a bounded experiment budget after the current Stage 1 gate; do not replace `NEXT_ACTION-001.md` yet.
- **Resume condition:** All activation fields in `CONTINUOUS_THEORY_AND_TEST_WORKFLOW.md` are approved and an `EVAL-###` row is preregistered before any confirmation run.
