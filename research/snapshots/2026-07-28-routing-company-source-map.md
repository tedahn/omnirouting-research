# Routing company source map — discovery snapshot

- **As of:** 2026-07-28
- **Status:** AI-assisted, source-checked discovery; individual company profiles still require reviewer promotion
- **Scope:** Public evidence for model/provider routing techniques, company activity, measured outcomes, counterevidence, and the reported Stripe–OpenRouter transaction
- **Comparator:** [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute)

## Bottom line

1. **Contradicted as stated:** Stripe has not publicly completed an OpenRouter acquisition. [The Information](https://www.theinformation.com/briefings/stripe-talks-buy-startup-openrouter/) and [Axios](https://www.axios.com/2026/07/24/stripe-openrouter-merger-ai-currency) report negotiations around a roughly $10B transaction, with no guarantee of a deal. Stripe said it does not comment on rumors; no completion announcement was found in the current [Stripe newsroom](https://stripe.com/newsroom/news) or [OpenRouter announcement feed](https://openrouter.ai/blog/announcements/). The correct label is **reported negotiations**.
2. **Grounded fact:** Stripe and OpenRouter already have a substantial commercial integration. OpenRouter uses Stripe for payments, invoicing, tax, and fraud controls; Stripe Projects can provision an OpenRouter account, API key, credentials, and billing. Sources: [Stripe partnership announcement](https://stripe.com/newsroom/news/openrouter-and-stripe) and [OpenRouter Stripe Projects documentation](https://openrouter.ai/docs/guides/overview/stripe-projects).
3. **Grounded implementation assessment:** OmniRoute is a useful open implementation of multi-factor operational routing, resilience, quota management, and fallback. Its `auto` path is heuristic scoring with epsilon-random exploration and table/pattern-based task fitness—not a demonstrated learned quality predictor. It has evaluation tooling but no committed result corpus establishing its broad quality/cost/latency claims.
4. **Strongest public company case found:** GitHub Copilot's HyDRA combines live system health with task-aware capability prediction. Its paper reports production deployment and reproducible coding-oriented outcomes. AWS supplies the next strongest first-party evaluation, but its router is limited to two same-family models and cannot learn from application-specific performance data. OpenRouter now publishes an Auto Beta method and small first-party benchmark suite, but independent evaluation and full cost distributions remain absent.
5. **Evidence warning:** dynamic routing is not one technique. Deterministic policy graphs, provider load/failover, task-aware model selection, cascades, global constrained allocation, and agent-level routing solve different problems. Comparing their percentage savings as one leaderboard would be invalid.

## Stripe and OpenRouter: verified state versus inference

| Statement | State | Evidence and interpretation |
|---|---|---|
| Stripe completed an OpenRouter acquisition | **Contradicted** | Current reporting says talks, not a signed or completed acquisition. No official completion announcement was found as of this snapshot. |
| Stripe is reported to be discussing an acquisition around $10B | **Corroborated report** | The Information and Axios independently report negotiations while retaining deal-failure caveats. This is not company confirmation. |
| OpenRouter uses Stripe commercially | **Grounded fact** | Stripe documents payments, invoicing, tax, fraud, usage tracking, and pricing/billing integration. |
| Stripe already performs task-aware cross-model selection | **Unsupported/overstated** | Stripe's token-billing/AI-gateway surface is adjacent metering and provider access; public documentation does not establish prompt-based quality routing. |
| A deal would combine inference routing with metering and economic infrastructure | **Inference** | Strategically plausible from the existing products and integration, but no post-transaction roadmap exists because no deal has been announced. |
| OpenRouter plans deeper enterprise and intelligent-routing investment | **Grounded source claim** | Its [Series B announcement](https://openrouter.ai/blog/series-b/) names enterprise controls, multimodal inference, and further intelligent-routing investment. This is OpenRouter's plan, not Stripe's. |

### Confirmation ladder for the transaction watch

Do not promote the status without crossing the corresponding evidence gate:

1. **Reported talks:** credible reporting with attributable sourcing.
2. **Signed/announced agreement:** official Stripe and OpenRouter announcement naming terms or transaction structure.
3. **Regulatory/closing process:** filings or official conditions and expected close.
4. **Completed acquisition:** both parties announce closing.
5. **Product roadmap:** dated, attributable product or engineering plan.
6. **Observed integration:** shipped documentation, APIs, migration behavior, pricing, and customer-visible controls.

## OmniRoute implementation audit

| Dimension | Evidence-backed assessment |
|---|---|
| Scope | MIT-licensed Node/TypeScript gateway with provider/account and cross-model routing; fast-moving release branch. |
| Implemented strategies | Priority, weighted, round-robin, power-of-two choices, least-used, quota/headroom/reset, cost, context/cache affinity, last-known-good path, auto, fusion, pipeline, and fallback strategies appear in docs and source modules. |
| Dynamic signals | Health/circuit state, quota, inverse cost, inverse latency, task fit, stability, tier, request specificity, context/cache/reset affinity, and connection density. |
| Learning claim | The public engine shows heuristic scoring and configurable epsilon-random exploration. Task fitness relies mainly on mappings and pattern boosts. No reward-updating learned router was established. |
| Resilience | Circuit behavior, cooldown, response-validation failover, session stickiness, and sampled shadow routing are implemented. |
| Evaluation | Exact/contains/regex/custom-function grading and baseline-comparison tooling exist. No committed outcome corpus demonstrating routing gains was found. Tool-call and LLM-judge evaluation appear absent from the documented evaluator. |
| Enterprise risk | Fusion/shadow modes can duplicate inference cost and prompt exposure; broad provider support increases policy, credential, data-residency, and compatibility burden. |
| Research use | Strong implementation reference for heuristic operational routing; weak evidence for independently demonstrated quality optimization or enterprise adoption. |

Primary code locations: [routing reference](https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.49/docs/routing/AUTO-COMBO.md), [scoring](https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.49/open-sse/services/autoCombo/scoring.ts), [strategy interface](https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.49/open-sse/services/autoCombo/routerStrategy.ts), [exploration engine](https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.49/open-sse/services/autoCombo/engine.ts), [task fitness](https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.49/open-sse/services/autoCombo/taskFitness.ts), [evaluation docs](https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.49/docs/frameworks/EVALS.md), and [evaluation code](https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.49/src/lib/routerEval/index.ts).

## Technique map

| Family | Representative systems | Decision mechanism | Best evidence found | Main limitation |
|---|---|---|---|---|
| Operational heuristic gateway | OmniRoute; LiteLLM Auto v2 | Weighted live signals, rules, pools, exploration, affinity, fallback | Public source code and configuration | Quality fitness is often heuristic; outcome validation is sparse |
| Provider telemetry routing | OpenRouter provider routing; OmniRoute; Cloudflare fallback | Outage, price, latency, throughput, quota, circuit state | Observable routing controls and telemetry docs | Selects an execution endpoint, not necessarily the best model response |
| Deterministic policy graph | Cloudflare Dynamic Routing; Portkey conditional routing | Metadata/parameter/content rules, percentages, budgets, rate limits | Versioned configurations, API schemas, rollback | Requires operator-authored policy; no demonstrated quality predictor |
| Binary weak/strong selector | RouteLLM; AWS Bedrock | Preference-trained classifier or response-quality predictor plus threshold | Reproducible RouteLLM; quantified AWS internal tests | Model-pair and workload drift; AWS restricts candidates and feedback |
| Multi-model trained ranker | Microsoft Foundry; Not Diamond; Martian | Prompt/task representation predicts quality or ranks candidates under cost/latency settings | Detailed product docs; partial benchmarks and vendor studies | Exact training/decision functions and independent production evidence vary |
| Task taxonomy plus revealed-usage ranking | OpenRouter Auto Beta | Classify into about 30 task types, rank by trailing seven-day task-level spend share, apply a cost-percentile filter, then configure fallbacks | Detailed current docs and three first-party benchmarks | Spend is popularity/revealed preference rather than direct per-request quality; independent evaluation is absent |
| Capability-requirement matching | GitHub Copilot HyDRA | Multi-head task requirements matched to configuration-defined model profiles | Production paper plus current product docs | Coding-heavy evaluation; model profiles remain an operational dependency |
| Global constrained optimizer | Academic OmniRouter | Capability/cost prediction followed by workload-level constrained allocation | Paper, code/data claim, explicit budgets/capacity | Later work reports weak accuracy-floor compliance under changing targets |
| SLA-aware or online policy | PROTEUS; WISERouter; TRACE-Router | Accuracy-target-conditioned policy or contextual bandit with feedback | Recent papers and reproducible benchmark designs | Research-stage; production overhead, drift, and safety remain open |
| Parallel ensemble/fusion | OmniRoute Fusion; OpenRouter Fusion | Multiple models answer; judge or synthesizer combines | Product implementations and selected evaluations | Multiplies cost, latency, data exposure, and correlated-judge risk |

## Priority company and project catalog

### Priority 1 — full profile and experiment

1. **GitHub Copilot / HyDRA** — strongest public production evidence. A ModernBERT encoder predicts reasoning, code, debugging, and tool-use requirements; profile-based shortfall matching chooses the cheapest sufficient model. The [paper](https://arxiv.org/abs/2605.17106), [product documentation](https://docs.github.com/en/copilot/concepts/models/auto-model-selection), and [engineering summary](https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/) should anchor the production profile.
2. **AWS Bedrock Intelligent Prompt Routing** — trained response-quality prediction between exactly two same-family models. Use the [current documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html) and [GA evaluation report](https://aws.amazon.com/blogs/machine-learning/use-amazon-bedrock-intelligent-prompt-routing-for-cost-and-latency-benefits/).
3. **OmniRoute** — inspectable heuristic gateway and resilience comparator. Treat scale and outcome language in the README as unverified until reproduced.
4. **OpenRouter** — separately profile [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection), [Auto model routing](https://openrouter.ai/docs/features/model-routing), and enterprise/governance controls. Auto Beta classifies prompts into about 30 task types, ranks models using trailing seven-day task-level spend share, filters candidates by a cost-percentile control, and adds fallbacks. Do not mix provider-level Exacto results with Auto model-selection evidence.
5. **RouteLLM / LMSYS** — reproducible weak/strong selection baseline using matrix factorization, similarity-weighted Elo, BERT, and causal-LLM classifiers. Sources: [repository](https://github.com/lm-sys/RouteLLM) and [paper](https://arxiv.org/abs/2406.18665).
6. **Academic OmniRouter plus PROTEUS** — pair the global constrained optimizer's [positive paper](https://arxiv.org/abs/2502.20576) with [PROTEUS counterevidence](https://arxiv.org/abs/2601.19402).

### Priority 2 — mechanism and evidence-gap profile

7. **Microsoft Foundry Model Router** — trained task/complexity router with Balanced, Cost, and Quality modes, model subsets, policy controls, and failover. Start with [concepts](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router) and its [evaluation guidance](https://devblogs.microsoft.com/foundry/how-to-run-evals-for-model-router/). Public customer-grade outcome evidence remains sparse.
8. **Cloudflare AI Gateway** — strong deterministic enterprise control plane with conditions, A/B splits, budget/rate limits, versioning, and rollback. It is not yet evidence of learned quality selection. Source: [Dynamic Routing](https://developers.cloudflare.com/ai-gateway/features/dynamic-routing/).
9. **Not Diamond** — pre-trained and custom input-to-model rankers using customer evaluation data and a cost-quality dial. Profile [training](https://docs.notdiamond.ai/reference/train_custom_router_v2_pzn_traincustomrouter_post), [selection](https://docs.notdiamond.ai/reference/token_model_select_v2_modelrouter_modelselect_post), vendor outcomes, and RouterArena counterevidence together.
10. **Martian** — proprietary `model mapping` router plus public RouterBench work. Start with [RouterBench](https://arxiv.org/abs/2403.12031) and preserve the distinction between a useful benchmark contribution and vendor product claims.
11. **LiteLLM Auto Routing v2** — close open-source comparator to OmniRoute, combining heuristic features, optional classifier, rules, tier pools, Thompson sampling, session affinity, and cause logs. Source: [Auto Routing documentation](https://docs.litellm.ai/docs/proxy/auto_routing). It is very new and lacks a published quality/cost evaluation.

### Monitor or verify before profiling

- **Google Vertex AI Model Optimizer:** the former surface appears experimental or redirected; confirm current availability, product ownership, candidate model pool, and evaluation before treating it as current.
- **NVIDIA routing blueprints:** the older LLM Router blueprint is deprecated and newer Switchyard/NeMo surfaces are experimental; monitor rather than synthesize as a stable enterprise offering.
- **Unify:** the current company surface documents an agent product with internal routing, while the older external LLM-router/evaluation surface appears absent. Treat old comparisons as historical until availability is confirmed.

## Outcome and counterevidence cards

These results are deliberately not combined into a ranking.

| System | Reported result | Setting and limitation | State |
|---|---|---|---|
| GitHub HyDRA | 75.4% SWE-bench Verified resolution versus 74.2% always-Sonnet at 12.9% savings; iso-quality reports 54.1% savings | Five-model coding pool; production paper; generalization reported on other coding/tool benchmarks | Grounded paper result; external production replication absent |
| AWS Bedrock | RAG tests report 63.6% average savings, 87% routed to Haiku, with baseline Sonnet accuracy maintained | AWS internal/public datasets; English-focused; exactly two models; no app-specific learning | Vendor-observed, not independent |
| RouteLLM | Up to 85% cost reduction while retaining 95% GPT-4 performance on MT-Bench | GPT-4-1106/Mixtral-era binary pair and benchmark; modern agent traffic needs revalidation | Reproducible research claim |
| OpenRouter Auto Beta | At quality setting: 83.8% GPQA, 74.0% tau-bench Airline, and 60.0 normalized DRACO versus deprecated Auto at 50.0%, 34.0%, and 19.6% | Vendor-run samples of 198 questions, 50 agent tasks, and 20 research reports; table omits total cost and selection distributions | Vendor-observed; no independent replication |
| Academic OmniRouter | Up to +6.30 percentage points accuracy and at least 10.15% cost reduction versus paper baselines | Workload-level constrained optimization; paper setting | Research result |
| PROTEUS evaluation of OmniRouter | OmniRouter met requested accuracy floors only 22% of the time | RouterBench/SPROUT runtime target test; later independent research team | Material counterevidence |
| RouterBench | Basic routers often failed to beat its zero-router baseline across tasks | 405K outcomes; older model pool; benchmark itself should be refreshed | Material counterevidence |
| RouterArena | No router led every metric; Not Diamond reached about 87% of best-model accuracy at about 171% of best-model cost in its setup | 26-model setup; configuration-sensitive; not a universal product verdict | Material counterevidence |
| OmniRoute | Evaluation tooling exists; no committed routing-result corpus found | Public repo inspection only | Unknown outcome |
| Cloudflare | No routing outcome study found | Product/control documentation | Unknown outcome |
| Microsoft Foundry | No sufficiently powered public customer study found in this pass | Microsoft recommends workload-specific evaluation | Unknown production outcome |

## What appears plausible next

These are hypotheses, not observed outcomes.

1. **Capability vectors replace scalar difficulty.** HyDRA's independent reasoning/code/debug/tool dimensions offer a stronger catalog-update story than pair-specific binary routers. Falsifier: comparable cross-domain tests show no benefit over a calibrated scalar selector.
2. **Routing expands from request-local to workload/SLA control.** OmniRouter, PROTEUS, and WISERouter suggest budgets, capacity, and explicit quality floors will become first-class inputs. Falsifier: online constraints add too much instability or operator burden in production.
3. **Agent routing becomes session- and cache-aware.** Long-horizon work rewards task pinning, cache boundaries, terminal rewards, and tool-use competence rather than independently switching every call. Falsifier: per-call switching consistently improves agent success after full cache and retry costs.
4. **The winning production architecture is layered.** A plausible stack combines policy eligibility, task capability, provider health/capacity, sticky execution, response verification, and escalation. Falsifier: end-to-end learned routers reliably dominate layered controls on governance, latency, and incident recovery.
5. **Evaluation becomes live and longitudinal.** Static one-turn benchmarks will be supplemented by SWE-bench/tau-bench-like agent tasks, shadow traffic, drift tests, and regret against changing model pools. Falsifier: static routing scores remain strongly predictive of live production outcomes.
6. **Commercial consolidation centers on control plus economics.** Stripe/OpenRouter talks, their existing integration, and gateway billing products make combined routing/metering/settlement strategically plausible. This is not a confirmed roadmap.

## Next evidence-gathering iteration

1. Freeze the cited mutable pages and exact repository commits.
2. Build six priority profiles using the common boundary map.
3. Extract each numerical result into one outcome record; capture judge, sample, price date, model pool, and confidence interval when available.
4. Run contradiction searches before writing cross-company synthesis.
5. Reproduce OmniRoute, RouteLLM, and one SLA-aware method on the same coding-agent workload.
6. Refresh the transaction claim daily and product surfaces every 14 days.
7. Stop the discovery expansion when two independent passes add neither a new mechanism nor a measured outcome category.

## Unresolved high-value questions

- Which models did OpenRouter Auto Beta select in each benchmark, what were the full cost and latency distributions, and does an independent task-level evaluation reproduce its results?
- How does HyDRA behave outside coding and tool-use workloads, under model-price changes, and after catalog additions?
- Can AWS and Microsoft routers meet domain-specific quality floors without application-specific retraining?
- Which production systems expose routing regret, fallback causes, policy eligibility, and cache effects in a way operators can audit?
- Do gateway-level routing gains survive full accounting for retries, duplicate calls, router inference, cache misses, and incident operations?
- If Stripe/OpenRouter negotiations become a signed deal, which routing, billing, settlement, procurement, and governance surfaces are actually announced rather than inferred?
