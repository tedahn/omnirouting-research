# VAL-RUN-006-01 — Synthetic confirmation result

## Identity and immutable linkage

- **Run ID:** `VAL-RUN-006-01`
- **Cycle ID:** `VAL-CYCLE-006-01`
- **Validation only:** Yes; this is not an OmniRouting scientific result
- **Theory artifact:** `runner/VAL-HYP-006-01-v1.md`
- **Theory SHA-256:** `3c39aa7e21a2643a24df2fddcf6407c88491291b60961c9e2cfa904bef667374`
- **Preregistration artifact:** `runner/VAL-EVAL-006-01-v1.md`
- **Preregistration SHA-256:** `a8512ca40fd2d8ece5a164ca86c06fe0339be80bab193b8ac3170f3188bec7b7`
- **Holdout SHA-256:** `5c29523d386e18555e5ed1eaede9105900c7f8dad85a17159ab0ec38a8381e83`
- **Independent evaluator:** Pending separate-context evaluation
- **Human reviewer:** Pending

The holdout digest matched the pre-reveal commitment, and `PREHOLDOUT_ARTIFACTS.sha256` still matched before analysis.

## Reproducibility record

- **Fixture:** `fixture/holdout.json`, eight synthetic full-information tasks
- **Frozen rule:** `low -> model_a`; `high -> model_b`
- **Analysis:** Deterministic complete enumeration; no sampling or model judgment
- **Baselines:** Always `model_a`; always `model_b`
- **Thresholds:** Exactly 100% success, at least 25% lower cost than always-`model_b`, and lower mean latency than always-`model_b`
- **Machine-readable output:** `runner/OBSERVATIONS.json`
- **External calls, spend, production traffic, and private data:** None

## Observed synthetic results

| Route | Success | Total cost units | Mean latency |
|---|---:|---:|---:|
| Frozen complexity gate | 8/8 (100%) | 20 | 162.5 ms |
| Always `model_a` | 4/8 (50%) | 8 | 112.5 ms |
| Always `model_b` | 8/8 (100%) | 32 | 212.5 ms |

Versus always-`model_b`, the frozen rule used 37.5% fewer cost units and had 50 ms lower mean latency while preserving 100% success on this committed synthetic fixture. All three frozen positive-path criteria were met.

## Classification

- **Controller-test classification:** `positive_path_criteria_met_pending_separate_evaluation`
- **Scientific classification:** Not applicable
- **Novelty or field claim:** None
- **Reason:** The observations validate deterministic controller plumbing against a synthetic fixture only; they do not support a real routing theory.

## Execution limitation

The isolated pre-holdout runner froze the theory and preregistration. An isolated post-holdout runner then encountered a workspace-relative manifest resolver error and did not persist artifacts before timeout. The root deterministic harness resumed from the frozen checkpoint, verified hashes, and produced this result without changing the rule or thresholds. This handoff is recorded as a workflow regression for human review, not hidden as a seamless single-run execution.

## Next gate

Separate-context evaluation must compare the transcript, hashes, observations, and all adversarial cases to `TEST_PLAN.md`. Human review remains required after that evaluation.
