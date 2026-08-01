# Conformal-routing integration and saturation test

- **As of:** 2026-07-29
- **Scope:** One bounded public-source delta: integrate the conformal-routing candidate from pass 3, then run one independent no-addition formulation.
- **Source boundary:** Public primary artifacts only.
- **Budget used:** 6 of 6 primary-source access operations, covering two unique artifacts; repeated ACL PDF extraction attempts are counted. No further source was opened after the stop trigger.
- **Supporting records:** SRC-065, CLM-033, CLM-034, MTH-017, OUT-024.
- **Refresh trigger:** New paper version, implementation release, independent replication, deployment-shift evidence, or adjudication of the carry-forward externality leads.
- **Decision use:** Stage 1 gate only; this snapshot does not authorize profiling, theory promotion, experimentation, or production adoption.

## Bottom line

The conformal candidate is now represented as the distinct but composable MTH-017 calibration family. It can sit on top of the pairwise predictor in MTH-003, but adds a held-out Clopper-Pearson threshold rule and a high-probability bound on the violation rate among cheap-routed queries. The bound is not per-query safety, content-safety policy, subgroup control, or deployment robustness.

The independent stakeholder-externality formulation then opened [GAR: Carbon-Aware Routing for LLM Inference via Constrained Optimization](https://arxiv.org/abs/2605.11603). Its primary abstract introduces per-request CO2 minimization using time-varying grid carbon intensity, accuracy floors, p95-latency constraints, and an online primal-dual rolling carbon budget. Those signals, objective, constraint set, and carbon endpoint are absent from the current ledgers, so the candidate is M4 material-method evidence and the Stage-1 stop rule fired. GAR is not yet ledgered.

## Conformal evidence integration

### Taxonomy decision

MTH-017 remains distinct from MTH-003. MTH-003 predicts whether a designated weak model is sufficient. MTH-017 calibrates a gate threshold against a user-selected violation tolerance and confidence level, routes nothing cheaply when no threshold is feasible, and can be composed with a pairwise predictor.

### Formal scope and assumptions

The paper's Section 3 selects the lowest threshold whose exact Clopper-Pearson upper confidence bound is at most alpha. Under exchangeability between calibration and test data, it states that the probability that routed-subset violation exceeds alpha is at most delta. The contract is limited by:

- held-out calibration data and a fixed binary violation definition;
- exchangeability and non-adaptive reuse of the calibrated rule;
- model-pair, task, alpha, delta, gate, and sample dependence;
- marginal control over calibration randomness rather than conditional subgroup control;
- possible loss of validity under deployment distribution shift; and
- expensive-model fallback when no feasible threshold exists.

### Exact reported outcome

Table 2 and Figures 2-3 use Mixtral-8x7B and GPT-4-1106-preview on 7,450 GSM8K and 14,042 MMLU queries, one stratified 55/15/15/15 split, and delta 0.10.

- GSM8K at alpha 0.30: conformal coverage 0.367, violation 0.280, and 35% savings; validation-tuned coverage 0.596, violation 0.317, and 58% savings, so the baseline crosses the bound.
- MMLU at alpha 0.20: conformal coverage 0.900, violation 0.191, and 87% savings; validation-tuned coverage 0.926, violation 0.196, and 90% savings.
- The alpha sweep spans 0.05 to 0.50. These are single-split offline results, not repeated reliability or production evidence.

## Independent no-addition formulation

This formulation was frozen before retrieval and searched stakeholder externalities rather than the pass-3 failure surfaces:

1. worst-group, equitable, or multi-tenant routing objectives;
2. incentive-compatible provider markets, user welfare, or strategic behavior; and
3. carbon-aware routing with directly measured emissions under quality or SLA constraints.

Metadata triage mapped EquiRouter to existing anti-collapse evidence. It also surfaced incentive-market and user-choice leads, but they were not opened or adjudicated because the carbon-family primary artifact triggered the mandatory stop. A new vendor, benchmark, or result magnitude alone would not have been material; GAR changes both the decision objective and measured externality.

## Gate decision

Stage 1 remains open. The latest material addition is now the unintegrated GAR candidate, so the two-formulation no-addition sequence resets after GAR is integrated. The proposed eight-profile queue remains unapproved, and this result is research priority rather than endorsement.

## Exactly one next action

Run one bounded GAR evidence-integration delta: inspect its exact method and result tables, separate carbon emissions from energy and monetary cost, decide whether it extends an existing constrained-routing family or requires a new family, and ledger only verified source, claim, method, and outcome evidence. Then run the first of two post-GAR independent no-addition formulations. Stop again on any material addition.
