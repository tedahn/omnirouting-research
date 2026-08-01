# GAR integration and post-GAR auction stop

- **Date:** 2026-07-29
- **Stage:** Stage 1 discovery
- **Gate:** `decisions/GATE-001-gar-public-source-integration.md`
- **Decision owner:** Workspace requester acting as research lead
- **Research status:** GAR integrated; first post-GAR formulation stopped on a material auction-based step-allocation candidate
- **Promotion status:** No Stage 2, theory, experiment, scheduler, or production promotion authorized

## Frozen inputs and authority

The run used `context-packs/CTX-001-gar-integration.md`, `briefs/PROFESSIONAL_PROMPT-gar-integration-2026-07-29.md`, and `briefs/PROFESSIONAL_PROMPT-post-gar-saturation-001-2026-07-29.md`. The working tree is based on Git commit `411447e22ca72b08d1fe82c1f82508b25a9051a5` and contains pre-existing uncommitted research work.

The human gate authorized public-primary GAR integration plus one independent formulation, with a cumulative maximum of six primary-source opens or 60 minutes. Three opens were counted: two accesses to GAR v1 during exact extraction and one access to Agora v1. Metadata queries did not consume the primary-open allowance. No private data, paid retrieval, author contact, experiment, profile, or deployment action occurred.

## GAR evidence integration

### Primary artifact

- **Artifact:** GAR: Carbon-Aware Routing for LLM Inference via Constrained Optimization
- **Version:** arXiv `2605.11603v1`, submitted 2026-05-12
- **Primary URL:** <https://arxiv.org/html/2605.11603v1>
- **Ledger records:** `SRC-066`, `CLM-035`, `CLM-036`, `MTH-018`, `OUT-025`

### Exact method disposition

GAR predicts correctness, p95 latency, and request carbon for each model. Its carbon estimator combines token-conditioned model energy with time- and region-dependent grid intensity. A feasibility gate enforces predicted accuracy and latency; the base variants minimize modeled carbon in the feasible set. GAR-PD adds a sliding-window primal-dual update for a rolling carbon budget. If no model is feasible, the algorithm considers the full pool and minimizes constraint violation.

This is registered as **MTH-018 Carbon-aware constrained model routing**. It is distinct from MTH-007's workload-level budget/capacity allocation and MTH-008's online SLA adaptation because carbon intensity is an explicit time-and-region-sensitive objective. It can be composed with those families. Energy in Wh or MJ, modeled grams CO2, and monetary cost remain separate quantities.

Primary locations: Sections 3.1-3.4, Equations 1 and 8-10, Algorithm 1, Section 4.4, and Appendix B Table 10.

### Exact outcome disposition

Across six datasets with 1,200 examples each and five candidate models, GAR-PD reports 0.737 macro accuracy, 0.712 modeled g CO2/request, and 703 ms. The largest-model baseline reports 0.741, 2.750 modeled g CO2/request, and 426 ms. The paper characterizes the carbon difference as a 74% reduction with comparable accuracy.

Primary locations: Section 4.1 Table 1, Section 5.1 Table 2, Section 5.2 Table 3, and Section 6.

### Limits preserved

- Carbon is modeled from energy and grid-intensity inputs, not directly measured production CO2 telemetry.
- Public grid data may lag by hours; regional accounting and predictor calibration can drift.
- The paper reports a 200-sample calibration split but does not clearly state whether that count is per dataset.
- Financial cost, uncertainty intervals, repeated seeds, independent replication, dynamic model pools, and a full regret analysis are absent.
- No public code repository was located in the primary HTML; code was not executed.

## Post-GAR formulation 001

### Frozen search surface

The independent formulation tested provider incentives, auction or market allocation, user choice and welfare, abandonment or re-prompting, and worst-group welfare. Queries were frozen before retrieval in `briefs/PROFESSIONAL_PROMPT-post-gar-saturation-001-2026-07-29.md`.

Metadata screening surfaced several leads. Unrelated advertising auto-bidding and career-path papers were excluded. Conformal Cascade and ContinuityBench appeared in the parallel metadata results but were not opened or adjudicated after the stop. The first in-scope incentive-allocation lead was opened:

- **Artifact:** Agora: Enhancing LLM Agent Reasoning Via Auction-Based Task Allocation
- **Version:** arXiv `2607.09600v1`, submitted 2026-07-10
- **Primary URL:** <https://arxiv.org/html/2607.09600v1>

### Materiality decision

**Material addition found; Stage 1 remains open.** Agora decomposes work into reasoning units, calibrates candidate-agent competence, assigns each unit by an auction-framed utility combining calibrated success and cost, executes the winners, composes the answer, and updates a post-hoc calibrator from evaluator feedback. This step-level calibrated allocation is not represented by MTH-009 parallel fusion, MTH-014 reinforcement-learned multi-round routing, or MTH-016 handoff/supervisor dispatch. A provisional **auction-based calibrated step-allocation** family therefore requires a separate integration decision.

The paper evaluates matched two-backend pools on MuSiQue-Ans, MMLU-Pro, SciCode, SPIQA, and MathVision. Reported examples include 71.9% MMLU-Pro accuracy versus a 68.1% best single-backend baseline, and 55.3 MathVision Pass@1 versus 54.6 for FrugalGPT. Its MMLU-Pro ablation reports 68.1% for one model, 70.0% with planning, and 71.9% with planning plus auction. These are paper-reported offline results, not independent validation.

Primary locations: Sections 3 and 4.1-4.4, Tables 2-4, Section 5.1 Table 6, Section 5.4 Figure 4, and Limitations.

### Negative evidence and unresolved questions

- The abstract calls the mechanism incentive-compatible, but the bounded inspection did not locate an exact payment rule, formal theorem, or strategic-agent experiment. That property remains a reported claim, not an accepted guarantee.
- Gains depend on calibrated competence, useful candidate complementarity, and valid planner decompositions; the paper directs fallback to the strongest agent under shift.
- The auction adds roughly `|tasks| × |agents|` short bid calls; the paper's two-agent, 2-3-unit settings add about 4-6 calls.
- Current evidence does not establish robustness to collusion, gaming, evaluator error, large candidate pools, production drift, or independent replication.
- The codebase mentioned by the paper was not located or pinned in this bounded run.

## Stop and handoff

The material-addition stop fired on Agora. Formulation 002 was not run, and carried incentive/user-choice leads were not further adjudicated. Saturation cannot be claimed.

Exactly one next human decision is proposed: **approve or reject a bounded public-source Agora integration delta that verifies its allocation rule, incentive-compatibility basis, evaluation denominators, cost accounting, and implementation artifact before restarting the two-formulation no-addition sequence.**

## Pinned post-GAR ledger state

| Artifact | Rows | SHA-256 |
|---|---:|---|
| `sources.csv` | 66 | `a0bfea16ed84084906d9df457575f1a4f5cde755f2fcf41a389fb58d74fc18f4` |
| `claims.csv` | 36 | `bf76fa7450b72e8e903989e5435886d006a84a348d92817608feb251906cc864` |
| `methodologies.csv` | 18 | `efbc3f59365fe14c17930d2c547dc78c30756030262f97fcbda0b8f5a371bc21` |
| `outcomes.csv` | 25 | `5f11c0e40914c97d94654ee1b087f55c48ece5afaf0baace5921af53d96f46dc` |

These hashes precede state, index, change-log, and validation-record edits made after the four scientific ledgers were frozen.
