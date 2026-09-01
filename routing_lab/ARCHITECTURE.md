# Agent-native routing lab architecture

## Boundary and assumptions

This build is a local reference harness for deterministic routing mechanics. It
does not call live models, run a scientific experiment, expose a production
endpoint, or alter the research workspace's current stage gate. Synthetic
fixtures make the executable path testable without credentials, spend, provider
drift, or claims about real model performance.

The shared filesystem is the state boundary:

```text
routing_lab/
├── workspace/              tracked, reviewable definitions
│   ├── models/             model and agent targets
│   ├── policies/           static or score-based policies
│   ├── objectives/         evaluation weights and hard guardrails
│   ├── workflows/          independently routed stage graphs
│   ├── cases/
│   │   ├── development/    optimizer may use train + validation
│   │   └── confirmation/   mutation protected; optimizer forbidden
│   ├── context.md          durable operator knowledge
│   └── state.json          active simulation policy and objective
└── runtime/                untracked, reproducible run artifacts
    ├── events/             append-only JSONL audit stream
    ├── runs/               evaluation reports
    ├── proposals/          optimization candidates
    └── completions/        explicit completion signals
```

## Decision path

Each request declares a route kind (`model` or `agent`), required capabilities,
complexity, risk, and optional cost/latency/allow/block constraints. The router:

1. discovers enabled targets from the catalog;
2. filters by kind, capability, policy eligibility, and hard request limits;
3. obtains per-target predictions from an evaluation case or the target priors;
4. applies static selection or a transparent weighted score;
5. applies the risk-specific quality floor and abstention threshold; and
6. returns the selected target, every exclusion, predictions, score, and reason.

Workflow stages use exactly the same primitive. The workflow declares stage
context; it does not hardcode a hidden routing workflow.

Cost and latency are normalized against request limits when present and against
versioned policy-owned reference bounds otherwise. This keeps efficiency terms
comparable instead of silently reducing them to zero on unbudgeted requests.

## Evaluation and optimization

Evaluation checks outcomes rather than a prescribed call sequence. Reports
include task success, abstention, hard violations, quality, total cost, cost per
success, cost/latency budget utilization, p50/p95/p99 latency, Brier score,
oracle selection accuracy, and oracle regret. Composite weights and guardrails
are versioned objective resources. The displayed score is transparent and
subordinate to raw metrics and hard guardrails; alternate objective records make
sensitivity checks reproducible.

Optimization is a bounded grid search over quality/cost/latency weights,
abstention, and risk floors. It fits on `train`, selects on `validation`, rejects
hard-regression candidates, records full-suite, evaluated-subset, policy, and
objective hashes, and emits a
pending proposal. It cannot read confirmation cases and cannot auto-activate.
Proposal application rechecks dataset, policy, and objective hashes and requires
a named human; it affects only local simulation state. The CLI records the
approver string but does not authenticate identity, so this is an attribution
gate rather than proof of authorization.

Raw CRUD cannot update or delete the active policy or objective; operators clone
them to new IDs and use the proposal path. Confirmation case reads, writes, and
evaluation also require an explicit flag at the CLI boundary. Direct filesystem
access remains possible, so these controls prevent accidents rather than provide
an authenticated security boundary.

## Architecture checklist

- **Parity — satisfied:** the CLI is the shared surface, and
  `CAPABILITY_MAP.json` maps every human action to the same agent-operable
  command.
- **Granularity — satisfied:** full resource CRUD remains available; route,
  evaluate, and optimize are inspectable domain shortcuts rather than gates.
- **Composability — satisfied:** new behaviors come from JSON targets, policies,
  workflow stages, cases, and the operator prompt without changing the engine.
- **Emergent capability — satisfied for the lab boundary:** arbitrary model or
  agent targets and unforeseen workflow stage combinations can be represented
  through catalog capabilities and request constraints.
- **Dynamic versus static external APIs — not yet applicable:** live external
  APIs are intentionally absent. Target discovery is dynamic through model CRUD;
  a future provider adapter must preserve discover/access primitives.
- **CRUD completeness — satisfied:** model, policy, objective, workflow, and case entities
  support create, read, update, and delete; destructive and confirmation actions
  are explicit.
- **Primitives, not workflows — satisfied:** resource and routing decisions are
  separate; workflows are data composed from the same routing primitive.
- **API as validator — satisfied for this boundary:** open string identifiers
  and capability names permit new targets; contracts validate shape and safety,
  not a hardcoded vendor list.
- **Shared workspace — satisfied:** humans and agents read and write the same
  tracked JSON files and untracked runtime artifacts.
- **`context.md` — satisfied:** durable operating knowledge is stored alongside
  the workspace.
- **File organization — satisfied:** entity-scoped directories and safe IDs make
  state directly inspectable.
- **Completion signals — satisfied:** `complete-task` writes an explicit record.
- **Partial completion — satisfied:** workflow results are `completed` or
  `partial`, with per-stage decisions suitable for resume.
- **Context limits — satisfied:** `context` returns bounded summaries and only
  ten recent events; full records are fetched on demand.
- **Available resources/capabilities — satisfied:** `context` and `capabilities`
  expose live state in user vocabulary.
- **Dynamic context — satisfied:** context is rebuilt from current files on each
  call.
- **Agent to UI/no silent actions — satisfied for the CLI:** there is no separate
  GUI; writes share the file service and append audit events immediately.
- **Capability discovery — satisfied:** both people and agents can request the
  current action map.
- **Mobile requirements — not applicable:** this is a local CLI harness.

## Extension boundary

A live adapter should accept the same request and return predicted and observed
target records. Add provider discovery, execution, credentials, budgets,
propensity logging, retries, and kill-switch enforcement as separate primitives.
Do not treat this simulator as permission to add them, and do not mix synthetic
and measured cases without explicit provenance and comparable units.
