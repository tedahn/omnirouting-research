# Research sprint 001 — routing techniques, company evidence, and Stripe/OpenRouter

- **Status:** Active bounded discovery
- **Authorized by:** Workspace requester on 2026-07-28
- **As of:** 2026-07-28
- **Boundary:** Public sources only; no vendor contact, paid-data export, private telemetry, or product recommendation
- **Decision unlocked:** Which routing families and entities deserve full profiles and representative experiments

## Research lanes

1. **Operational gateway routing:** OmniRoute, LiteLLM, Cloudflare, Portkey, and OpenRouter provider routing. Determine what is rules, scoring, telemetry, fallback, exploration, or actual learning.
2. **Learned model selection:** GitHub Copilot HyDRA, AWS Bedrock, Microsoft Foundry, RouteLLM, Not Diamond, Martian, and OpenRouter Auto. Extract the decision function and training/evaluation disclosure.
3. **Global and SLA-constrained routing:** academic OmniRouter, PROTEUS, WISERouter, and related work. Test whether global budgets and explicit quality floors change the operating model.
4. **Transaction and strategy watch:** Stripe/OpenRouter. Track the difference between the verified commercial integration, reported negotiations, a signed agreement, closing, and any post-transaction roadmap.
5. **Enterprise evidence:** look for production deployments, governance controls, data residency, failure behavior, operational burden, and independently checkable outcomes—not customer-logo counts.

## Iterative information-gathering loop

### Pass 1 — freeze and classify

- Save an `as_of` snapshot of mutable docs, releases, product status, model pools, pricing, and transaction reporting.
- Split routing into model, provider, policy, capacity, modality/tool/agent, and fallback decisions.
- Create candidate records even when evidence is weak; preserve exclusions and stale surfaces.

### Pass 2 — extract mechanisms

For every included system, record decision locus, candidate set, granularity, signals, decision mechanism, objective, learning mode, execution pattern, fallback, feedback loop, and known failure modes. Read code or papers when product language does not distinguish heuristics from learning.

### Pass 3 — normalize evidence

Create one outcome card per metric. Require a baseline, workload, model pool, judge/grader, sample, price date, latency context, result, and limitations. Keep vendor-internal, reproducible benchmark, independent replication, and production observation separate.

### Pass 4 — challenge

Search explicitly for failed quality floors, expensive routing, drift, stale routers, session inconsistency, cache loss, tool-call failures, privacy/data-residency conflicts, duplicated prompt exposure, and operator complexity. Run the same search against the strongest apparent result.

### Pass 5 — reproduce

Reproduce three contrasting approaches on one controlled workload:

1. deterministic/heuristic gateway baseline;
2. learned per-request selector;
3. constrained or SLA-aware selector.

Use frozen responses where licensing permits, then a small live canary. Report quality, cost, p50/p95 latency, routing regret, fallback rate, cache effects, policy violations, and stability after a model-pool change.

### Pass 6 — synthesize and redirect

- Rank **research value**, not vendors.
- Convert each unresolved high-value question into a retrieval query, code inspection, experiment, or monitoring trigger.
- Promote a conclusion only when its evidence threshold is met; otherwise keep the gap visible.

### Pass 7 — refresh

- Transaction watch: daily until the reported talks resolve.
- Active products and model pools: every 14 days or on release.
- Fast-moving techniques: every 30 days.
- Papers and stable concepts: on contradiction or annually.

## Search protocol

Run architecture-oriented and problem-oriented queries independently. Search official documentation, source repositories, papers, system/model cards, release notes, engineering posts, and named-builder talks before commentary. For every positive claim, add a paired query using `failure`, `limitation`, `regression`, `quality floor`, `cost overrun`, `drift`, `outage`, `deprecated`, or `benchmark leakage`.

Deduplicate syndicated coverage to its upstream report. A primary vendor source proves what the vendor said or shipped; it does not independently prove the claimed business or performance outcome.

## Exit criteria

Stage 1 is complete when:

- two independent discovery passes add no material decision mechanism or outcome category;
- every priority-one entity has a qualifying primary artifact;
- transaction status is labeled with the strongest available verb;
- the strongest positive case and at least three countercases are recorded;
- gaps in enterprise production evidence are explicit; and
- the next three experiments have owners, budgets, and stop rules.

## Immediate queue

1. Profile GitHub Copilot HyDRA, AWS Bedrock, OmniRoute, OpenRouter, RouteLLM, and academic OmniRouter/PROTEUS.
2. Reproduce OmniRoute's heuristic `auto` scoring against a fixed priority/fallback baseline on a small coding-agent trace.
3. Build a modern RouterArena-style test using current models, long-horizon coding tasks, and cache-aware cost accounting.
4. Monitor Stripe and OpenRouter official feeds plus the originating transaction reports; do not rewrite `reported negotiations` as an acquisition before a signed or completed deal is announced.
