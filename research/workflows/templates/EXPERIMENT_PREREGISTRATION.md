# EVAL-[next-id]-v1 — [experiment title]

## Immutable identity

- **Evaluation ID:** `EVAL-###`
- **Version:** `v1`
- **Hypothesis artifact:** `research/theories/HYP-###-vN.md`
- **Protocol version:**
- **Evidence snapshot ID:**
- **Preregistered at:** [ISO 8601, before confirmation results]
- **Owner:**
- **Independent falsifier:**
- **Independent evaluator:**
- **Replication owner:**
- **Frozen specification hash:** [compute before execution]

After the hash is frozen, do not change endpoints, thresholds, exclusions, splits, analysis, or stop rules. An amendment creates `vN+1`, links `supersedes`, and remains exploratory until independently confirmed. Every result card references the exact frozen hash.

## Question and estimand

- **Research question:**
- **H0:**
- **H1:**
- **Estimand and unit of analysis:**
- **Causal assumptions:**
- **Minimum meaningful effect or equivalence margin:**
- **Promotion threshold:**

## Design

- **Intervention:**
- **Control:**
- **Inclusion and exclusion rules:**
- **Target workload and fixtures:**
- **Exploration split and hash:**
- **Untouched confirmation split and hash:**
- **Temporal/OOD replication split and hash:**
- **Holdout custodian and access rule:**
- **Model/provider pool and version policy:**
- **Cache, rate-limit, and provider-state controls:**
- **Blocking or interleaving over time:**

## Baselines

- **Static best:**
- **Cheapest:**
- **Random eligible:**
- **Rules-based:**
- **Current router:**
- **Oracle:** [only when every candidate outcome is observed]

## Outcomes and analysis

- **Primary metric:**
- **Secondary metrics:**
- **Hard safety, policy, privacy, reliability, and tail-latency guardrails:**
- **Uncertainty interval or posterior:**
- **Sample size or power rationale:**
- **Seeds:**
- **Multiple-testing correction:**
- **Subgroups and worst-case analysis:**
- **Missing-data and failure handling:**
- **Equivalence, non-inferiority, harm, or superiority decision rule:**

For bandit feedback, declare logged selection propensities, overlap/positivity diagnostics, effective sample-size threshold, clipping and sensitivity analysis, and the preregistered IPS or doubly robust estimator. Do not report oracle regret without full candidate outcomes.

## Leakage and independence controls

- **Theorist access boundary:**
- **Evaluator blinding:**
- **Prompt/data contamination checks:**
- **Independent implementation plan:**
- **Model-family or human-review separation:**

## Budget, execution, and stop rules

- **Allowed tools and environment:**
- **Token budget:**
- **Dollar budget:**
- **Wall-time budget:**
- **Early stop rule:**
- **Abort and kill-switch conditions:**
- **Rollback:**

## Linked records

- **Evaluation ledger row:** `research/eval-cases.csv#EVAL-###`
- **Run/result cards:** `research/results/RUN-###.md`
- **Cycle checkpoint:** `research/cycles/CYCLE-###.md`
