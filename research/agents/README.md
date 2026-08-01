# Human-decision advisory agents

These role cards define on-demand AI advisors for the G0-G6 research process. They are prompts and authority contracts, not autonomous decision-makers or persistent human substitutes.

| Card | Role | Primary gates |
|---|---|---|
| `GATE_NAVIGATOR.md` | Identify the next narrow gate and assemble one packet | G0-G6 |
| `EVIDENCE_METHODS_CHALLENGER.md` | Challenge provenance, contradictions, comparisons, falsifiers, and validity | G1-G5 |
| `BOUNDARY_SENTINEL.md` | Check authority, privacy, safety, spend, operations, and adoption boundaries | G0, G4, G6 |
| `BLIND_EVALUATION_ASSISTANT.md` | Support frozen, blinded scoring without claiming independence | G5 |
| `GATE_CLERK.md` | Deterministically validate and persist an explicit human decision | G0-G6 |

The core council contains three AI advisors: Gate Navigator, Evidence and Methods Challenger, and Boundary Sentinel. Blind Evaluation Assistant is optional G5 support. Gate Clerk is a deterministic role, not an LLM advisor. Instantiate only the roles required by `../workflows/HUMAN_DECISION_AGENT_COUNCIL.md`. Every advisory run must satisfy `ADVISORY_CARD_TEMPLATE.md`. Use isolated, minimum-necessary context, merge by evidence provenance rather than vote count, and record same-model reviews as advisory. Before a second or later handoff, Gate Clerk also requires a human-attested checkpoint of the immediately preceding terminal event.

For the current Agora G0 decision, use only Gate Navigator and Boundary Sentinel, then the Gate Clerk after an explicit human decision. Invoke Evidence and Methods Challenger at G1/G2, after the bounded delta produces evidence to review. Do not invoke the Blind Evaluation Assistant.
