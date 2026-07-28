# Methodology: omni routing and dynamic model selection

- **Version:** 1.0
- **As of:** 2026-07-27
- **Status:** Ready for owner review
- **Owner:** Research lead (identity unresolved)

## Operational definitions

Use these definitions as research controls, not claims about the market:

- **Omni routing:** selection across more than one execution dimension—such as model, provider, modality, tool, agent, region, or fallback path—under explicit quality, cost, latency, reliability, policy, or capacity constraints.
- **Dynamic model selection:** choosing a model or execution path per request, task, user, or workflow stage using observed signals or feedback rather than only a fixed configuration.
- **Company exploration:** attributable company work supported by a public primary artifact. Marketing language alone is a discovery lead, not evidence of methodology or outcome.
- **Outcome:** a reported or independently observed result tied to a defined metric, baseline, workload, evaluation setting, and time window.
- **Plausible future:** a dated forecast with mechanism, drivers, barriers, leading indicators, falsifiers, probability or range, and resolution rule.

## Boundary map

Classify every candidate before comparison:

1. **Decision locus:** application, gateway, provider, model, agent/orchestrator, or infrastructure.
2. **Selection target:** model, provider, modality, tool, agent, region, or execution strategy.
3. **Granularity:** tenant, workflow, stage, request, token, or fallback event.
4. **Signal:** metadata, prompt/content features, embeddings, classifier output, historical performance, live telemetry, user policy, or capacity.
5. **Decision mechanism:** static rule, scorecard, supervised classifier, learned ranker, cascade, contextual bandit, reinforcement learning, search/planning, or hybrid.
6. **Execution pattern:** single selection, sequential cascade, speculative/parallel execution, ensemble, or escalation.
7. **Optimization target:** quality, cost, latency, reliability, safety, privacy, sovereignty, capacity, or a constrained multi-objective function.
8. **Learning loop:** none, offline retraining, online feedback, bandit update, human review, or adaptive policy.

Do not compare candidates assigned to materially different boundary categories without explaining why the comparison is valid.

## Company inclusion protocol

A company enters `company-landscape.csv` as a **candidate** after one attributable discovery source. It becomes **profiled** only when at least one Tier A or B artifact supports its relationship to routing. Examples of qualifying artifacts include official technical documentation, a paper, a repository, a model/system card, a detailed engineering report, a reproducible demo, or a named builder presentation with concrete method details.

Keep companies, products, research projects, and open-source communities as separate entity types. Do not infer production adoption from a prototype, benchmark, partnership, investment, or product announcement.

### Sampling

Build the universe broadly, then choose a stratified sample that covers different decision loci, mechanisms, objectives, company types, and evidence maturity. Do not select only well-known vendors or companies with favorable published results. Preserve excluded and negative cases with reasons.

Stop expanding the initial universe when two independent discovery passes add no material mechanism category, the major strata have at least one evidenced candidate, or the approved budget is reached.

## Evidence collection protocol

For each profile:

1. Capture the smallest faithful company claim and exact source location.
2. Trace secondary reporting to its upstream artifact.
3. Describe the mechanism using the boundary map; leave missing fields Unknown.
4. Record the evaluation design, baseline, workload, metric definition, reported result, and limitations separately.
5. Search for independent replication, contradiction, failure reports, and conditions where the method should not work.
6. Separate demonstrated behavior, vendor-reported outcome, inference, and forecast.
7. Assign evidence state, `as_of`, `refresh_by`, and decision relevance.

Repeated coverage of the same upstream claim counts once. A primary source establishes attribution, not independent confirmation of a broad performance claim.

## Outcome normalization

Normalize only when metric definitions and evaluation settings are compatible. Record at least:

- task success or quality and grader type;
- cost per request, successful task, or token;
- latency distribution, not only an average;
- routing regret or oracle gap when available;
- fallback, escalation, abstention, and failure rates;
- reliability, robustness, drift, and recovery behavior;
- policy, safety, privacy, and regional constraints;
- operator complexity and feedback/retraining cost.

When baselines, units, workloads, or time windows differ, present side-by-side evidence instead of a synthetic ranking. Never turn missing metrics into zeros.

## Future scenario protocol

Create forecasts only after the current evidence map is stable enough to expose drivers and constraints. Use two horizons by default: 12–24 months and 24–48 months. Each scenario must include a causal mechanism, probability or range, leading indicators, barriers, falsifiers, affected architecture layers, decision relevance, and a date or event that can resolve it.

Distinguish:

- **Continuation:** current evidenced mechanisms become cheaper, broader, or easier to operate.
- **Convergence:** gateways, providers, and orchestrators adopt similar selection surfaces or evaluation standards.
- **Discontinuity:** a new model, pricing structure, regulation, hardware constraint, or protocol changes the routing problem.
- **Constraint-dominant:** reliability, governance, data location, or switching costs limit technically plausible routing.

Do not infer inevitability from funding, attention, product launches, or benchmark gains.

## Synthesis gate

The first synthesis may recommend deeper research or an experiment only when:

- the company universe has documented coverage and exclusions;
- each material methodology category has primary evidence or is marked Unknown;
- outcome comparisons expose baseline and setting differences;
- the strongest countercase and failed/negative evidence are present;
- forecasts are separated from observed outcomes;
- every recommendation names the evidence that would reverse it.
