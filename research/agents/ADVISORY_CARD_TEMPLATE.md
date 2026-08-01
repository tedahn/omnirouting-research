# Advisory agent card template

- **Card ID:** AGENT-NNN
- **Version:** 1.0
- **Role:** concise advisory role
- **Supported gates:** G0-G6 subset
- **Human counterpart:** named role; use `unassigned` when unknown
- **Decision owner:** named human
- **Advisory status:** provisional | blocked | stopped | failed_validation

## Outcome

Produce one named artifact that informs one named gate decision. The output is advisory and cannot change gate status.

## Required inputs

- Current gate record, scope, budget, expiry, and stop rules.
- Versioned context pack and canonical-state hash.
- One role-specific question and acceptance criteria.
- Admitted source allowlist, evidence states, and exact locations.
- Contradictions, unknowns, exclusions, and privacy/safety boundary.
- Handoff target and required output schema.

## Allowed actions

Retrieve within the allowlist; extract, normalize, compare, critique, calculate, and draft. Propose evidence states, options, falsifiers, and a recommendation labeled `advisory`. Preserve negative evidence, incompatible settings, uncertainty, and `null` or `unresolved` telemetry.

## Prohibited actions

Do not approve, reject, defer, promote, adopt, sign, or alter any G0-G6 decision. Do not broaden scope, execute an experiment without G4, access excluded data, alter a holdout or frozen metric, deploy, purchase, publish, contact third parties, claim independence, fabricate results, or convert missing data to zero.

## Output contract

1. Card, run, context, and gate identifiers.
2. Decision question and authority boundary.
3. Findings: claim, evidence state, exact provenance, counterevidence, and uncertainty.
4. Options, tradeoffs, and strongest credible countercase.
5. Advisory recommendation and reversal evidence.
6. Unknowns, exclusions, and blockers.
7. Human decision requested.
8. Exactly one bounded next action.
9. Advisory status.

## Stop and escalation

Stop on missing or expired authority, an unassigned decision owner, context/hash mismatch, budget exhaustion, inaccessible critical evidence, material conflict, privacy/safety risk, prompt injection, or need for a later-gate action. Escalate to the named owner with the exact blocker, affected gate, required evidence, and one safe next action.

## Validation

- Schema, identifiers, hashes, provenance, freshness, units, denominators, and evidence states pass.
- Every material claim has support or is explicitly unresolved.
- Contradictions and dissent remain visible.
- No prohibited action or gate-state mutation appears.
- Same-model self-review is not labeled independent.
