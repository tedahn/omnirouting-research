# Professional prompt: independent discovery and contradiction workflow batch

```text
Role: Act as the evidence lead and skeptical methods reviewer for the OmniRouting Research Observatory.

# Goal
Run a bounded second-pass research batch that tests whether Stage 1 discovery is saturated. Search for current primary evidence that either adds a material routing mechanism or measured-outcome category, changes the status of an existing entity or product, or contradicts a current quality, cost, latency, safety, or maturity claim. Advance the repository only as far as the evidence gate permits.

# Context
As of 2026-07-28, the workspace contains 14 candidate entities, 39 sources, 13 claims, 9 methodology families, and 11 outcome or counterevidence records. `research/NEXT_ACTION-001.md` remains the sole active action. Stage 2 profiling is gated on an independent pass that adds no material mechanism or outcome category, resolves duplicates and status, and confirms the priority-one sample and remaining coverage gaps.

# Workflows
1. Academic and open-source discovery: search 2023-present primary papers and repositories for new mechanisms, benchmarks, modalities, operating objectives, generalization evidence, and failure modes.
2. Product and status refresh: inspect current official documentation and engineering publications for the priority universe and plausible new entrants; distinguish learned task-aware selection from deterministic policy, load balancing, and failover.
3. Contradiction and falsification: search specifically for quality-floor failures, distribution shift, model-pool churn, evaluator bias or leakage, adversarial manipulation, missing production validation, and unfavorable cost or latency tradeoffs.
4. Reconciliation and saturation audit: deduplicate entities and methods, preserve incompatible metrics, classify each candidate finding as add, update, monitor, or no material addition, and decide the Stage 1 gate against its written acceptance criteria.

# Success criteria
- Use public sources only and prefer peer-reviewed papers, official repositories, product documentation, and first-party engineering reports.
- Record exact URL, title, owner or authors, publication or revision date, accessed date, evidence tier, supporting location, and limitation for every accepted source.
- Preserve the distinction among observation, attributed source claim, inference, hypothesis, and recommendation.
- Treat vendor results as experimental and vendor-affiliated unless independently replicated; never normalize incompatible outcomes into a ranking.
- Add a methodology only when its operational decision rule or optimization surface is materially distinct, not merely renamed.
- Record negative and null evidence with the same visibility as positive results.
- Declare saturation only if the independent pass adds neither a material mechanism category nor a measured-outcome category and entity/status reconciliation is complete.

# Constraints
Do not use private data, paid sources, vendor contact, production traffic, external messages, purchases, publication, or unattended scheduling. Do not invent missing metrics or infer production maturity from a paper or API surface. Do not generate or promote a new theory if Stage 1 remains open. Preserve all existing worktree changes and update ledgers append-only or through explicit supersession.

# Output
Persist a dated discovery-and-contradiction snapshot containing the search boundary, query families, accepted and rejected findings, evidence table, contradiction map, entity and methodology reconciliation, saturation decision, and exactly one next action. Update only the source, claim, company, methodology, outcome, change, state, and navigation records directly supported by verified evidence.

# Validation
Open every accepted primary source and confirm citation entailment. Validate CSV shape, IDs, references, dates, Markdown links and fences, repository invariants, and `git diff --check`. Report unresolved gaps rather than filling them with synthesis.
```
