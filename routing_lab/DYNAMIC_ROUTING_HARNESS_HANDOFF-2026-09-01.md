# Dynamic routing harness design handoff

- **Handoff ID:** `ROUTING-LAB-DESIGN-001`
- **Version:** 1.0
- **Built at:** 2026-09-01T11:20:26Z
- **Status:** Advisory design input; implementation and live execution are not authorized by this document
- **Owner:** Workspace requester acting as research lead
- **Consumer:** Maintainer implementing the next `routing_lab` contract, router, evaluator, and evidence-store increment
- **Supported decision:** Which requirements and tests should enter the next simulation-only harness milestone
- **Canonical local state:** `contracts.py`, `router.py`, `evaluator.py`, `optimizer.py`, `store.py`, `cli.py`, objective resources, workspace fixtures, tests, and harness documentation as observed at the build timestamp
- **Primary external input:** OpenRouter, “How to Choose the Best AI Model (Live, in Your Editor),” published 2026-08-25
- **Context budget:** This design packet plus exact source and code pointers; retrieve external details only when a requirement depends on them
- **Refresh trigger:** A material harness-schema change, a live-data integration proposal, a major model/router release, or 30 days before using vendor pricing, rankings, or endpoint telemetry

## Decision and success criteria

The next harness increment should make dynamic-routing policies comparable on the work they are intended to perform, under frozen inputs and explicit quality, cost, latency, reliability, safety, and policy constraints. It should not select a production model merely because that model is popular, inexpensive per token, or highly ranked on a general benchmark.

This handoff succeeds when the implementing maintainer can:

1. map every proposed change to an existing module or a new inspectable resource;
2. distinguish hard eligibility constraints from soft optimization objectives;
3. calculate end-to-end cost per completed task, including failed attempts and fallback execution;
4. compare a dynamic router against meaningful fixed and oracle baselines on the same frozen cases;
5. reproduce a report from pinned case, target, policy, scorer, and telemetry snapshots; and
6. stop without a production recommendation when evidence is synthetic, stale, underpowered, policy-invalid, or not better than the strongest eligible fixed baseline.

## Authority boundary

### Authorized by this handoff

- Use these requirements to design schemas, fixtures, deterministic evaluators, and simulation tests.
- Preserve current `simulation_only` behavior.
- Add read-only adapters later if a separate implementation decision authorizes them.
- Treat vendor usage, benchmark, price, and endpoint data as dated inputs with provenance.

### Not authorized by this handoff

- Billable inference, web search, model evaluation, provider authentication, or MCP connection.
- Live traffic, shadow traffic, production routing, automatic scheduling, or policy promotion.
- Changes to the governed research ledgers, `CURRENT_STATE.md`, GATE-002, or the human handoff ledger.
- A claim that OpenRouter, its Auto Router, any model, or the local harness is production-superior.
- Treating the article's product guidance or worked examples as independent outcome evidence.

This is a design handoff, not an authority-bearing event in `research/handoffs.csv`.

## Executive design rule

Optimize the **smallest reliable execution plan for a defined task**, not a model name.

The routing decision must be a function of a versioned task contract, eligible target snapshot, policy, predictions with uncertainty, and current-enough operational evidence. The evaluation decision must be a function of frozen cases, realized attempt chains, explicit scorers, hard-constraint results, and named baselines.

Benchmarks and usage rankings may nominate candidates. Only task-representative confirmation evidence may support a harness promotion decision.

## Current harness state to preserve

| Existing property | Why it matters | Exact location |
|---|---|---|
| JSON-compatible, human- and agent-inspectable contracts | Avoids a hidden schema and makes fixtures reviewable | `routing_lab/contracts.py`, module contract |
| Capability, allowlist, blocklist, cost, latency, route-kind, and enabled-state eligibility checks | Establishes hard filtering before scoring | `routing_lab/contracts.py:65-134`; `routing_lab/router.py:29-55` |
| Risk-specific quality floors and explicit abstention | Prevents soft cost or latency preferences from overriding a minimum predicted success threshold | `routing_lab/contracts.py:82-112`; `routing_lab/router.py:99-131` |
| Deterministic candidate records with exclusion reasons | Makes each route decision explainable and testable | `routing_lab/router.py:88-144` |
| Per-stage routing for model and agent workflows | Preserves stage-level specialization instead of forcing one model for an entire workflow | `routing_lab/router.py:159-225` |
| Train, validation, and confirmation partitions | Supplies the skeleton for development versus final confirmation | `routing_lab/contracts.py:157-177` |
| Confirmation-case mutation guard | Reduces accidental holdout contamination | `routing_lab/store.py:193-198` |
| Dataset and policy hashing | Supports reproducibility and change detection | `routing_lab/store.py:133-146`; `routing_lab/evaluator.py:141-150` |
| Success, hard violations, abstention, quality, total cost, cost per success, p50/p95/p99 latency, oracle regret, oracle selection accuracy, and Brier score | Already measures several routing-level outcomes instead of only response quality | `routing_lab/evaluator.py:118-140` |
| Versioned balanced, efficiency-first, and quality-first objective resources | Separates declared development tradeoffs from evaluator code and pins the selected objective in reports | `routing_lab/workspace/objectives/`; `routing_lab/evaluator.py`, `_objective` and report manifest |
| Bounded grid-search proposals with separate human-attributed application | Keeps development search separate from activation and rejects confirmation-suite input | `routing_lab/optimizer.py`, `optimize_policy` and `apply_proposal` |
| Shared JSON CLI and capability discovery | Gives humans and agents the same inspectable surface for context, resources, routes, workflows, evaluation, proposals, and completion | `routing_lab/cli.py`; `routing_lab/CAPABILITY_MAP.json` |
| Dynamic bounded context | Exposes current targets, policies, workflows, suites, boundaries, and recent events without loading every artifact | `routing_lab/context.py` |
| Isolated behavioral test suite | Covers contracts, CRUD, confirmation mutation protection, model/agent/workflow routing, baseline comparison, optimization isolation, proposal review, stale hashes, context parity, and the JSON CLI | `routing_lab/tests/test_routing_lab.py` |
| Simulation-only state and explicit synthetic-evidence limitation | Prevents a development harness from being mistaken for a live router | `routing_lab/store.py:115-128`; `routing_lab/evaluator.py:141-155` |

## Current implementation gaps that affect interpretation

These are observations about the current untracked harness tree, not completed defects or authorization to fix them.

1. **Cost and latency weights need explicit normalization.** When a request omits `max_cost_usd` or `max_latency_ms`, `_score` uses each candidate's own prediction as its denominator. Both efficiency terms become zero, so those weights do not distinguish candidates (`routing_lab/router.py:58-68`).
2. **Fallback is a selection label, not an execution chain.** Static routing may choose a fallback when the default is ineligible, but the harness does not represent a failed first attempt followed by retry, escalation, or provider failover (`routing_lab/router.py:112-121`).
3. **The score policy does not use `fallback_target`.** The contract requires it for every policy, but scored selection does not execute it after a failure or abstention.
4. **Cost per success is promising but incomplete.** It includes the costs of routed failures in the numerator, which is useful, but cases contain one selected outcome rather than an attempt chain. Router overhead, retries, fallbacks, tools, search, repair, and human-review cost are absent (`routing_lab/evaluator.py:118-133`).
5. **The versioned objective still needs complete cost and latency semantics.** It penalizes mean budget utilization only when a request declares the corresponding maximum; otherwise utilization is recorded as zero. Absolute cost, tail latency, and end-to-end retry latency can therefore differ without affecting the objective. Raw metrics are correctly declared authoritative, so promotion should remain Pareto- and constraint-based.
6. **Optimizer promotion is narrower than the needed routing claim.** It now consumes the versioned objective's hard-violation and success-regression guardrails, meaningful-improvement threshold, and hash; it ranks safe candidates by the composite objective and uses total cost as a tie-breaker. Promotion still lacks strongest, cheapest, and fastest fixed-target comparator families and explicit abstention, tail-latency, calibration, regret, and slice-regression gates.
7. **The reported dataset hash covers the full suite, not necessarily the evaluated partition subset.** When `partitions` filters cases, `dataset_sha256` still hashes the entire suite (`routing_lab/evaluator.py:60-63,141-150`). Optimizer train and validation results therefore carry the same suite hash rather than exact subset hashes.
8. **Calibration is scored only for the selected target.** Candidate-level calibration, uncertainty, and conservative lower bounds are not measured.
9. **Latency is one scalar.** Time to first token, inference duration, queuing, tool time, retry delay, and end-to-end completion time are not separated.
10. **Audit events are append-only but not tamper-evident.** They have no previous-event hash, run-manifest hash, or trusted terminal checkpoint (`routing_lab/store.py:148-167`).
11. **CLI flags are local safety affordances, not human gate evidence.** `--allow-confirmation` and a non-empty `--approved-by` value enforce useful friction, but do not identify an authenticated decision record. Preserve the documented simulation-only boundary.
12. **Current tests establish the reference harness, not the P0 evidence model.** All 14 tests passed at the final observation point. The suite does not yet exercise attempt chains, fixed-target comparator families, partition-specific hashes, candidate calibration, fallback accounting, missing outcomes, end-to-end latency, or tamper-evident manifests.

## Evidence index

| ID | State | Source/version | Exact location | Supports or contradicts | Freshness |
|---|---|---|---|---|---|
| E01 | vendor-reported guidance | OpenRouter model-selection tutorial, 2026-08-25 | [Article](https://openrouter.ai/blog/tutorials/choose-best-ai-model/) | Task-specific selection; benchmarks shortlist; local prompts decide; cost per completed task; periodic reevaluation | Refresh on article or linked-doc change |
| E02 | vendor-reported product mechanics | OpenRouter tutorial, “The tools you'll use” and six-step framework | [Article](https://openrouter.ai/blog/tutorials/choose-best-ai-model/) | Dated usage, benchmark, provider, price, latency, and generation-cost inputs can be queried and tested | Volatile; verify before integration |
| E03 | vendor-reported router mechanics | OpenRouter tutorial, Step 6 | [Auto Router docs](https://openrouter.ai/docs/guides/routing/routers/auto-router) | Per-request task classification and routing can be a comparator | Volatile; not independent quality evidence |
| E04 | vendor-reported evaluation tooling | OpenRouter tutorial, Step 4 | [Ori Eval docs](https://openrouter.ai/docs/guides/ori/eval) | Eval-as-code, baselines, repeatability, and CI cadence are useful patterns | Volatile; do not execute without a separate decision |
| E05 | observed local implementation | `routing_lab/contracts.py` | Lines 65-177 | Existing target, policy, request, prediction, outcome, and case contracts | As of 2026-09-01 |
| E06 | observed local implementation | `routing_lab/router.py` | Lines 29-156 | Hard filtering, score selection, abstention, and decision evidence | As of 2026-09-01 |
| E07 | observed local implementation | `routing_lab/evaluator.py` | Lines 29-155 | Existing outcome validity, metrics, hashes, and synthetic limitation | As of 2026-09-01 |
| E08 | observed local implementation | `routing_lab/store.py` | Lines 115-167 and 193-223 | Simulation-only state, hashing, audit events, and confirmation guard | As of 2026-09-01 |
| E09 | observed local implementation | `routing_lab/optimizer.py` | `optimize_policy` and `apply_proposal` | Bounded development search, versioned objective guardrails and threshold, validation selection, stale dataset/policy/objective checks, and local human-attributed application | As of build timestamp |
| E10 | observed local interface | `routing_lab/cli.py`, `context.py`, and `CAPABILITY_MAP.json` | Full files | Shared JSON control surface, dynamic context, confirmation flag, proposals, and explicit completion | As of 2026-09-01 |
| E11 | observed local validation | `routing_lab/tests/test_routing_lab.py` | Fourteen test methods | Current contracts, holdout mutation guard, routing behavior, optimizer isolation, stale proposals, context parity, and CLI validation | As of build timestamp |
| E12 | observed local objective contract | `routing_lab/workspace/objectives/`; `routing_lab/evaluator.py` | Three objective JSON files; `_objective`; report manifest | Versioned development tradeoffs and objective hashing are now represented | As of build timestamp |
| E13 | source-backed local research conclusion | `research/claims.csv` | `CLM-010` | No examined router dominates every workload and constraint | Refresh with new confirmation evidence |
| E14 | source-backed local boundary | `research/claims.csv` | `CLM-013` | OpenRouter spend share is a popularity/revealed-preference signal, not a direct per-request quality estimate | Refresh with mechanism change |
| E15 | source-backed local counterevidence | `research/claims.csv` | `CLM-020`, `CLM-022`, `CLM-025`, and `CLM-026` | Route manipulation, judge bias, OOD behavior, collapse, rare experts, and failure to beat fixed baselines are material harness tests | Refresh by cited claim dates |
| E16 | source-backed local boundary | `research/claims.csv` | `CLM-032` | Provider/model fallback changes execution behavior and may change policy, quality, and data handling | Refresh with provider docs |
| E17 | research control | `research/METHODOLOGY-omni-routing.md` | “Outcome normalization” | Compare success, total cost, latency distribution, regret, fallback, robustness, policy, and operating complexity without converting missing metrics to zero | Stable until methodology revision |

## What the OpenRouter article contributes

### 1. Replace “best model” with a task contract

The harness should not accept a generic `task_type=coding` as sufficient. A useful task contract names:

- input shape and modality;
- expected output and format;
- scorer and acceptance threshold;
- tool-use or schema requirements;
- context-length distribution;
- risk tier and policy/data boundary;
- cost and latency service objectives; and
- the declared tradeoff when quality, cost, and latency conflict.

The task contract should be immutable for a confirmation run. Changing the rubric, prompt wrapper, context strategy, or candidate pool creates a new run lineage.

### 2. Use external rankings as discovery priors, not labels

Benchmarks, public arenas, and usage rankings reduce search cost. They do not supply the ground-truth label for a local case. A popularity-ranked candidate can enter the pool, but the routing predictor and evaluation outcome must be derived from the frozen local task.

Record for every nomination:

- source and query/filter;
- observation window;
- task taxonomy and version;
- rank, score, or share with its denominator;
- access time; and
- whether the signal measures quality, adoption, spend, tokens, latency, or something else.

Never merge these different signals into an unlabeled “quality” value.

### 3. Model selection and provider selection are different layers

The same model may be served by multiple providers with different prices, quantization, throughput, latency, uptime, supported parameters, data policies, and regions. The target identity should therefore be at least:

`model family/version + provider endpoint + execution variant + snapshot ID`

The harness should be able to evaluate:

- a fixed model and provider;
- a fixed model with provider failover;
- task-aware model routing;
- model routing followed by provider routing; and
- a managed external router as a black-box comparator.

Do not attribute provider failover gains to task-aware model selection.

### 4. Evaluate real work, especially known failures

A representative suite needs routine, difficult, malformed, ambiguous, long-context, policy-sensitive, and distribution-shifted examples. Toy prompts establish plumbing, not routing value.

The confirmation set should remain hidden from policy optimization. Independent evaluation requires more than a new prompt or a second run in the same context; preserve scorer separation, hidden labels where applicable, and a mutation-protected confirmation manifest.

### 5. Make cost per completed task the economic unit

Use token price only as an input. The reportable unit is:

```text
total cost per completed task =
  sum(router + all attempts + fallbacks + tools/search + repair + review costs)
  / accepted completed tasks
```

Also report cost per 1,000 completed tasks. When there are no completed tasks, emit `null` plus `undefined_reason=no_successes`; do not report zero.

The attempt model must capture failed calls and discarded outputs because they consume money and latency. If human repair or review is not monetized, report its count and duration separately as unresolved operational cost.

### 6. Treat reevaluation as policy lifecycle management

Target catalogs, prices, models, provider health, and task distributions drift. Each promotion record needs:

- `as_of` timestamps for volatile inputs;
- refresh/expiry rules;
- triggers for model, provider, price, policy, taxonomy, or workload changes;
- a challenger-versus-incumbent confirmation path; and
- a safe rollback or abstention state.

Scheduling reevaluation is a later operational capability, not implied authority to run it.

## Requirements for the next harness contract

### P0 — required before a meaningful confirmation comparison

1. **Versioned task contract.** Add `task_contract_id`, `task_type`, `input_modality`, `output_contract`, `scorer_id`, `success_threshold`, `risk`, and policy/data constraints.
2. **Endpoint-level target snapshot.** Separate stable target identity from dated price and telemetry. Include model version, provider, endpoint or route variant, capabilities, context limit, supported parameters, region/data policy, and `observed_at`.
3. **Explicit prediction provenance.** Predictions need predictor ID/version, training cutoff, feature schema, observation window, point estimates, uncertainty, and freshness. `Unknown` must remain representable.
4. **Attempt-chain outcome.** Replace the one-outcome assumption with ordered attempts containing selected model/provider, reason, status, tokens, cost components, timing components, policy result, and accepted/discarded state.
5. **Constraint-first routing.** Apply capabilities, data policy, geography, safety eligibility, context fit, and risk floors before utility scoring. Re-check them for every fallback.
6. **Defined normalization.** Cost and latency scoring require policy-owned reference bounds or candidate-set normalization pinned in the run manifest. No self-denominator default.
7. **Required baselines.** Evaluate the same cases against the strongest eligible fixed target, cheapest eligible fixed target, fastest eligible fixed target, current static policy, abstain/escalate policy, and an offline oracle. Add random or popularity routing only when analytically useful.
8. **Frozen comparison matrix.** Every candidate must have an outcome or an explicit missingness reason for every scored case. Do not treat missing outcomes as failures or zeros without a preregistered rule.
9. **Partition-correct integrity.** Hash the exact evaluated case IDs, content, target snapshot, policy, predictor, scorer, and partition. Report both suite hash and evaluated-subset hash when they differ.
10. **Promotion by constraints and Pareto evidence.** A scalar objective may guide development, but promotion requires all hard gates and a visible quality/cost/latency/reliability comparison against baselines.

### P1 — required before interpreting routing as robust

1. Candidate-level calibration: Brier score, reliability curve, and calibration error by target and task slice.
2. Confidence-aware routing: use conservative bounds or abstain when prediction uncertainty is too large.
3. Slice reporting: task subtype, difficulty, risk, context length, modality, language, tool use, and known failure class.
4. OOD and temporal splits with drift indicators and an explicit retraining/expiry rule.
5. Route-share and collapse diagnostics so a router that nearly always selects one target is compared directly with that fixed target.
6. Rare-expert and oracle-gap diagnostics to measure whether specialization is actually captured.
7. Route-integrity tests: prompt manipulation, category shortcuts, policy inversion, unavailable endpoint, and poisoned/stale telemetry.
8. Separate time-to-first-token, generation time, queue time, tool time, retry delay, and end-to-end completion latency.
9. Reliability metrics: provider error, timeout, refusal, malformed output, retry, fallback, and recovery rates.
10. Workflow metrics: stage success, end-to-end workflow success, cumulative cost/latency, critical-stage failures, and cascading error attribution.
11. Judge validity: deterministic checks where possible; otherwise scorer versioning, blinded assessment, disagreement, label balance, and judge-bias diagnostics.
12. Repeated trials where sampling or provider variance exists; report dispersion and paired uncertainty rather than a single run.

### P2 — later capabilities, separately gated

1. Read-only catalog and telemetry adapters that cache raw dated snapshots before normalization.
2. Eval-as-code generation from approved fixtures, with human review before execution.
3. Shadow replay against authorized non-sensitive traffic.
4. Controlled challenger scheduling and rollback.
5. Managed routers, including `openrouter/auto-beta`, as black-box comparators under the same task contract and accounting boundary.
6. Online learning or bandit updates with propensity logging, delayed-feedback handling, safety constraints, and a kill switch.

## Proposed inspectable resource shapes

These are field-level design proposals, not final schemas.

### `task_contract`

```text
id, version, task_type, description
input: modalities, context_length_distribution, sensitive_data_class
output: format, schema, tool_contract, acceptance_rubric
constraints: risk, data_policy, regions, max_total_cost_usd,
             max_end_to_end_latency_ms, min_success_probability
tradeoff: lexicographic gates or named utility profile
scorer_id, scorer_version, owner, created_at, expires_at
```

### `target_snapshot`

```text
target_id, model_id, model_version, provider_id, endpoint_variant
capabilities, supported_parameters, context_limit, quantization
price: input, output, request, tool/search, currency, units
telemetry: ttft, throughput, e2e_latency, uptime, error_rate, window
policy: data_retention, training_use, regions, safety_constraints
source, observed_at, refresh_by, content_sha256
```

### `prediction`

```text
case_id, target_snapshot_id, predictor_id, predictor_version
pass_probability, quality_distribution, expected_cost, expected_latency
uncertainty, calibration_snapshot_id, feature_schema_version
predicted_at, valid_until, provenance
```

### `attempt`

```text
attempt_id, parent_run_id, case_id, sequence
route_decision_id, target_snapshot_id, trigger
started_at, first_token_at, completed_at
input_tokens, output_tokens, reasoning_tokens, cached_tokens
inference_cost, router_cost, tool_cost, repair_cost
status, failure_class, policy_violation, accepted
generation/provider trace IDs when authorized
```

### `evaluation_run_manifest`

```text
run_id, mode=simulation_only, task_contract_sha256
case_suite_sha256, evaluated_subset_sha256, target_snapshot_sha256
policy_sha256, predictor_sha256, scorer_sha256, code_revision
partitions, baselines, seeds, started_at, completed_at
authority_record, data_boundary, limitations, parent_run_id
```

## Evaluation protocol

### Phase A — define and freeze

1. Name one shippable task or one explicitly stratified workload.
2. Define acceptance, hard constraints, cost boundary, latency boundary, and failure taxonomy.
3. Freeze development, validation, and confirmation manifests.
4. Freeze scorer and judge instructions before confirmation outputs are inspected.

### Phase B — shortlist

1. Apply capability, policy, context, modality, and region filters.
2. Use current benchmarks and usage rankings only to nominate a bounded pool.
3. Record the signal's actual meaning and time window.
4. Include at least one cheap, one fast, and one high-quality plausible candidate when eligible.

### Phase C — build the outcome matrix

1. Collect or simulate every candidate on the same frozen cases and execution settings.
2. Record all attempts, errors, refusals, retries, fallbacks, and missing cells.
3. Measure realized cost and timing rather than reconstructing them from list price when exact data exists.
4. Keep exploration outputs out of confirmation-policy training.

### Phase D — develop the router

1. Train or configure only on allowed partitions.
2. Calibrate predicted success and uncertainty.
3. Compare candidate-set and policy changes separately.
4. Preserve exclusion reasons and the full candidate record for every decision.

### Phase E — confirmation

1. Run the locked policy once on the mutation-protected confirmation set.
2. Compare paired outcomes with every required baseline.
3. Report hard violations first, then success/coverage, cost, latency, reliability, calibration, and regret.
4. Report slices and negative results; do not average away critical-risk failures.

### Phase F — decision

Promote only if:

- all hard constraints pass;
- the router beats the strongest eligible fixed baseline on a preregistered primary measure or provides a justified Pareto improvement;
- gains survive relevant slices and uncertainty analysis;
- fallback and abstention behavior remains policy-valid;
- the evidence snapshot is current; and
- a named human approves the next authority-bearing gate.

Otherwise retain the incumbent, revise the experiment, or stop with `insufficient_evidence`.

## Required metrics and denominators

| Metric | Required definition |
|---|---|
| Task success rate | Accepted completed tasks / all eligible cases; name scorer and threshold |
| Coverage | Non-abstained cases / all eligible cases |
| Selective success | Accepted completed tasks / non-abstained cases; report beside coverage |
| Cost per completed task | Total costs from all cases and all attempts / accepted completed tasks |
| Cost per 1,000 completed tasks | `cost_per_completed_task * 1000`; unresolved if no successes |
| End-to-end latency | Request entry to accepted result, including retries and tools; p50/p95/p99 |
| Hard violation rate | Cases with any policy, privacy, safety, cost, or latency hard violation / all cases |
| Fallback and retry rates | Cases entering each path / routed cases, plus success and cumulative cost by path |
| Abstention rate | Abstained cases / all eligible cases; include reasons |
| Calibration | Brier and calibration error for all candidate predictions and selected predictions |
| Oracle regret | Predeclared objective gap to a feasible offline oracle; state what the oracle knows |
| Fixed-model delta | Paired success, cost, latency, and violation difference from each required fixed baseline |
| Route concentration | Target call share and entropy; compare dominant selection with that fixed target |
| Stability | Decision flip rate under repeated calls, prompt-preserving perturbations, and telemetry refreshes |
| Operational overhead | Router latency/cost, snapshot refresh work, evaluator/judge cost, and human-review load |

Never compare metrics whose workloads, model pools, units, baselines, or windows differ without showing them side by side.

## Task-specific evaluation guidance

| Workload | Primary success contract | Important additional checks |
|---|---|---|
| Coding | Tests, task completion, tool correctness, and review rubric | Repository context, multi-file changes, security cases, flaky-test handling, tool reliability |
| Summarization | Coverage and faithfulness against source | Long-context distribution, input cost, citation correctness, omission/hallucination checks |
| Structured extraction | Schema validity and field-level correctness | Missing/ambiguous fields, malformed input, retry rate, deterministic validation |
| Chat or assistant | User/task success under a latency SLO | TTFT, refusal appropriateness, conversational consistency, safety, escalation |
| Vision or multimodal | Domain-specific correctness | Modality eligibility, real screenshots/images, OCR/detail failures, input pricing |
| Agentic workflow | End-to-end task success | Stage attribution, tool-call validity, cumulative budget, loops, recovery, partial completion |

## Contradiction and tradeoff register

| Tension | Evidence on one side | Counterevidence or limitation | Harness disposition |
|---|---|---|---|
| Usage share is useful | Current use can surface viable candidates quickly | Spend or token share measures adoption and economics, not direct local quality | Use as a discovery prior only |
| Benchmarks are efficient | They bound a very large catalog | Benchmark tuning, judge bias, task mismatch, and stale model pools can mislead | Shortlist, then test frozen local cases |
| Cheap tokens reduce cost | Unit price is part of every call cost | Retries, verbose outputs, tools, fallbacks, and repair can reverse the result | Optimize total cost per completed task |
| One model is operationally simple | A clear winner on a narrow stable task can be a good fixed policy | Mixed tasks and model churn can reward routing | Require fixed baselines; route only when incremental value is demonstrated |
| Automatic fallback improves resilience | Failover can recover provider errors | It may change model behavior, safety policy, data handling, cost, and latency | Re-evaluate eligibility and account for every fallback attempt |
| Live telemetry improves routing | Current latency and availability can prevent bad endpoint choices | Short windows are noisy and make runs hard to reproduce | Snapshot telemetry, record windows, and test sensitivity |
| A weighted score simplifies selection | Transparent weights are easy to inspect | Compensation can hide a hard failure, and normalization changes rankings | Hard gates first; use weights only inside the feasible set |
| A composite eval score aids iteration | It can rank development variants | It hides tradeoffs and can omit material economics | Never use it as the sole promotion criterion |
| An external auto-router is a useful comparator | It represents a maintained per-request routing policy | Its pool, classifier, and internal signals may drift or be opaque | Treat as a dated black box, not an oracle |

## Failure taxonomy the harness should preserve

- `no_eligible_target`
- `abstained_low_confidence`
- `capability_mismatch`
- `context_limit_exceeded`
- `policy_or_data_boundary_violation`
- `predicted_budget_exceeded`
- `provider_unavailable`
- `timeout_before_first_token`
- `timeout_during_generation`
- `provider_or_model_error`
- `refusal_expected` / `refusal_unexpected`
- `malformed_output`
- `tool_call_invalid`
- `scorer_rejected`
- `retry_budget_exhausted`
- `fallback_exhausted`
- `stale_target_snapshot`
- `missing_outcome`
- `measurement_failed`

Do not collapse `measurement_failed`, `missing_outcome`, or `abstained` into model failure. Do not count a recovered fallback as a first-attempt success.

## Minimum regression suite for the implementation pass

1. Hard policy exclusions always run before scoring.
2. A cheap but policy-ineligible target can never win through weights.
3. Cost and latency affect ranking even when the request has no explicit maximum, using a pinned normalization rule.
4. Missing predictions produce an explicit unresolved/abstain path or a documented fallback estimator.
5. A low-confidence prediction triggers abstention at the configured threshold.
6. Every fallback attempt rechecks capability, policy, region, cost, and latency eligibility.
7. Failed and discarded attempts contribute to total cost and end-to-end latency.
8. Cost per completed task is `null` with a reason when success count is zero.
9. Evaluation of a partition records the exact evaluated-subset hash.
10. Confirmation fixtures cannot be changed without explicit authorization and a new manifest lineage.
11. A dynamic policy is compared against all required fixed baselines on identical cases.
12. A router that selects one model nearly always is flagged and compared with that fixed policy.
13. Candidate-level calibration is measured, not only selected-target calibration.
14. Missing outcomes are reported and cannot silently become zero-quality outcomes.
15. P95 and P99 include retry and fallback delay in end-to-end mode.
16. An audit/run manifest can reproduce policy, code, data, scorer, target, and telemetry inputs.
17. Synthetic fixtures cannot emit a production-readiness or model-superiority status.
18. Package import and CLI entry points either resolve or fail with a deliberate, tested unavailable-feature message.

## Recommended implementation sequence

### Milestone 1 — make the evidence unit correct

- Add task, target-snapshot, attempt-chain, scorer, and run-manifest contracts.
- Correct normalization and partition hashing.
- Preserve current simple fixtures through an explicit schema migration or compatibility adapter.
- Add the required fixed baselines and total-cost accounting.

**Exit condition:** a simulation report is fully reproducible and reports end-to-end cost per completed task without live calls.

### Milestone 2 — make comparisons trustworthy

- Add candidate-level calibration, uncertainty, slice metrics, route concentration, rare-expert/oracle diagnostics, and repeated-trial support.
- Add route-integrity, OOD, malformed-input, and fallback regressions.
- Replace single-score promotion with hard gates plus a Pareto comparison.

**Exit condition:** the harness can show when routing does not beat a fixed target and can explain why.

### Milestone 3 — add bounded freshness adapters

- Add read-only importers for catalog, pricing, provider, ranking, and generation telemetry.
- Cache raw responses with provenance before normalization.
- Keep unavailable fields `null`/`unresolved`; reject expired snapshots when policy requires freshness.

**Exit condition:** a dated external snapshot can be replayed offline without contacting a provider.

### Milestone 4 — request a separate live/shadow gate

- Define data boundary, spend cap, target pool, secrets handling, rate limits, stop conditions, holdout owner, reviewer, and rollback.
- Only then consider live evaluation, an external auto-router comparator, or scheduled reevaluation.

**Exit condition:** a named human gate authorizes exactly one bounded run; this handoff does not satisfy that condition.

## Material unknowns

- The target workload and its primary success rubric are unresolved.
- The intended candidate model/provider pool is unresolved.
- Whether the next milestone remains fully synthetic or may ingest dated read-only external telemetry is unresolved.
- The cost assigned to human review and repair is unresolved.
- The required data regions, retention rules, and privacy constraints are unresolved.
- The independent confirmation-set custodian and evaluator are unresolved.
- The acceptable statistical uncertainty and minimum effect size are unresolved.
- The proposed P0 evidence contracts, accounting, comparator, and integrity regressions remain absent from the current 14-test suite.
- No live OpenRouter ranking, price, endpoint, or generation record was retrieved in this pass.

## Excluded context

| Item | Reason | Reconsider when |
|---|---|---|
| Current model winners or prices | Volatile and unnecessary for the design decision | A bounded candidate-selection run is approved |
| OpenRouter authentication or billable calls | Not required to produce a design handoff | A live-evaluation gate names a spend cap and data boundary |
| Automatic policy activation | The bounded optimizer exists, but current promotion evidence and CLI attribution are not an authority-bearing production gate | P0 evidence contracts and baselines pass and a later gate defines activation authority |
| Production telemetry and customer prompts | Data boundary and privacy approval are unresolved | A named owner approves a shadow/live protocol |
| Changes to research ledgers or GATE-002 | The current governed Stage-1 action concerns Agora, not harness implementation | The research lead opens a separate evidence-admission decision |

## Validation status at handoff

| Check | Result | Interpretation |
|---|---|---|
| `python3 -m routing_lab validate` | Passed: 5 models, 2 policies, 1 workflow, 3 objectives, and 12 cases | Current resource contracts and active simulation state resolve |
| `python3 -m unittest discover -s routing_lab/tests -v` | Passed: 14 tests | Current contracts, routing, optimizer, proposal, context, and CLI behaviors pass their reference suite |
| `python3 scripts/validate_gate.py` on GATE-001 and GATE-002 | Passed | Both gate records are structurally valid; GATE-002 remains `proposed` |
| `python3 scripts/validate_workspace.py` | Failed | Pre-existing governed handoff drift: GATE-001 issuance `decision_hash` does not match the current gate file |
| `python3 scripts/validate_handoffs.py` | Failed | Same GATE-001 hash mismatch; `CHECKPOINT-001` is also still `pending_human_signature` |
| Live provider/model execution | Not run | No performance, price, ranking, or production claim was generated |

The handoff did not repair or rebaseline governed state, apply a proposal, evaluate confirmation cases, or alter active simulation policy. The temporary article scrape was removed after synthesis; the public source URL remains in the evidence index.

## Validation requirements for the next consumer

Before implementing, the maintainer should confirm:

- every local path and cited claim ID still resolves;
- the harness remains `simulation_only`;
- the exact target workload and scorer are named;
- P0 schema changes have migration and regression coverage;
- evaluated-subset, policy, target-snapshot, scorer, and code hashes are recorded;
- the fixed-baseline matrix is complete;
- volatile inputs have `as_of`, source, and refresh rules;
- negative, missing, and contradictory evidence remains visible; and
- no report can translate synthetic evaluation into a production or superiority claim.

## Stop and fallback rules

Stop the implementation or evaluation and return an explicit unresolved status when:

- the task or success criterion changes after confirmation inputs are exposed;
- the target pool, policy, scorer, or telemetry snapshot changes without a new run lineage;
- candidate outcomes are materially missing or use incompatible settings;
- a hard safety, privacy, regional, cost, or latency boundary is crossed;
- evidence is stale under the declared refresh policy;
- the router does not beat the strongest eligible fixed baseline and no preregistered Pareto benefit exists;
- the result depends on an unverified external claim; or
- live execution, credentials, spend, private data, or production authority would be required.

The safe fallback is the named incumbent/static policy, explicit abstention/escalation, or `insufficient_evidence`—never an inferred production promotion.

## Exact consumer task

Use this handoff to prepare an implementation plan for **Milestone 1 only**. Map each P0 requirement and regression to concrete changes in `contracts.py`, `router.py`, `evaluator.py`, `optimizer.py`, `store.py`, `cli.py`, fixtures, and deliberately added tests or modules. Preserve inspectable JSON resources, the shared human/agent CLI, deterministic simulation, hard eligibility gates, abstention, confirmation protection, bounded proposal review, raw metrics, and current authority boundaries. Do not run models, connect OpenRouter, activate routing, edit governed research state, or claim a model/router winner. Return changed files, schema migration notes, regression results, remaining unknowns, and the first unmet gate.
