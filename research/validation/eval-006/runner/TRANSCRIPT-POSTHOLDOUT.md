# EVAL-006 runner transcript — POS-01 post-holdout

## Authorization and integrity checks

The confirmation fixture was written only after `VAL-HYP-006-01-v1.md` and `VAL-EVAL-006-01-v1.md` were frozen.

- Holdout commitment expected: `5c29523d386e18555e5ed1eaede9105900c7f8dad85a17159ab0ec38a8381e83`
- Holdout file observed: `5c29523d386e18555e5ed1eaede9105900c7f8dad85a17159ab0ec38a8381e83`
- Commitment decision: Match
- Theory hash decision: Match
- Preregistration hash decision: Match
- Pre-holdout transcript hash decision: Match

No rule, endpoint, comparator, or threshold changed after reveal.

## Deterministic execution

The frozen rule selected `model_a` for four `low` tasks and `model_b` for four `high` tasks.

- Frozen route: 8/8 success, 20 cost units, 162.5 ms mean latency
- Always-`model_a`: 4/8 success, 8 cost units, 112.5 ms mean latency
- Always-`model_b`: 8/8 success, 32 cost units, 212.5 ms mean latency
- Cost reduction versus always-`model_b`: 37.5%
- Mean-latency reduction versus always-`model_b`: 50 ms

The synthetic positive path met every frozen criterion. No unobserved value was estimated.

## Resumability event

The first isolated post-holdout runner identified that its initial hash resolver treated repository-relative sidecar paths as validation-directory-relative. It reported the issue but did not write a result before timeout. The run was stopped, and the root deterministic harness resumed from the immutable artifacts, corrected only path resolution, recomputed the same committed fixture, and persisted the observed values.

This event did not change the hypothesis, routing rule, holdout, thresholds, or analysis. It remains a recorded workflow regression because the positive path was completed across a checkpoint handoff rather than by one uninterrupted runner.

## Boundary result

- No scientific claim or novelty claim was made.
- No private data, production traffic, external tool, purchase, publication, or scheduler was used.
- No independent-evaluator or human-review status was claimed.
- Result state: `positive_path_criteria_met_pending_separate_evaluation`.
