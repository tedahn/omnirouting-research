# Professional prompt: continuous OmniRouting theory and experiment workflow

```text
Role: Act as a research-systems architect for the OmniRouting Research Observatory.

# Goal
Extend the existing repository with a durable, bounded workflow that lets ChatGPT repeatedly gather high-value evidence, generate genuinely testable theories about omni routing and dynamic model selection, design the cheapest decisive tests, and improve its own research-routing policy without treating model output as evidence or allowing unbounded self-modification.

# Context
The repository already separates sources, claims, methods, outcomes, assumptions, evaluations, forecasts, and protocol changes. Preserve that governance and invoke the existing seven-pass `research/RESEARCH_SPRINT-001.md` rather than duplicating it. The workflow must be usable manually in a ChatGPT Project and later by an external API scheduler, while remaining honest about the fact that a model does not persist or self-trigger without surrounding orchestration and durable state.

# Success criteria
- Define an inner scientific loop for evidence gathering, anomaly mining, competing theory generation, prior-art review, falsification, preregistration, execution, blind evaluation, and replication.
- Define an outer meta-routing loop that assigns research subtasks to appropriate models or deterministic tools and evaluates those assignments on validated information gain, calibration, reproducibility, cost, and latency.
- Make every proposed theory mechanism-level, falsifiable, decision-relevant, provenance-linked, and paired with a rival explanation and kill test.
- Separate theory generation, experiment execution, and grading; never describe same-model personas as independent validation.
- Reuse `assumptions-forecasts.csv`, `eval-cases.csv`, `claims.csv`, `sources.csv`, `outcomes.csv`, and `change-log.csv` rather than creating overlapping ledgers.
- Include cadence, budgets, stop conditions, human approval gates, novelty labels, routing-specific metrics, and a resumable checkpoint contract.
- Supply a copy-ready prompt that runs exactly one bounded cycle per invocation.
- Demonstrate the controls with a synthetic dry run that makes no scientific claim and stops when required execution inputs are absent.

# Constraints
Keep the current Stage 1 gate and the single owned `NEXT_ACTION` intact. Preserve all existing worktree changes. Public-source research and local drafting are in scope; private data, spending, publication, external contact, production traffic, system changes, and unattended scheduling require explicit approval. Do not optimize for positive findings or the word “groundbreaking.” Candidate novelty must survive prior-art review, fresh-data replication, independent grading, and expert review before any field-level novelty claim. Null, negative, inconclusive, and measurement-failure results must remain visible.

# Output
Create:
1. a repository workflow document;
2. a copy-ready one-cycle ChatGPT controller prompt;
3. a synthetic validation record;
4. narrow discoverability and upload-manifest updates; and
5. protocol evaluation and change-log entries.

# Validation
Run the workspace validator and `git diff --check`. Confirm that a missing owner, workload, budget, data boundary, holdout custodian, or independent evaluator stops execution at the appropriate gate. Confirm that no generated theory, model judgment, or synthetic dry-run result is promoted as evidence.
```
