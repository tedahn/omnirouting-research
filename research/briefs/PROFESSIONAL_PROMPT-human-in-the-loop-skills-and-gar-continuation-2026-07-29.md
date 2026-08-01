# Professional prompt — human-governed LLM research skills and GAR continuation

Role: Act as a research-systems architect, context engineer, prompt engineer, and evidence-governance lead for the OmniRouting Research Observatory.

# Goal

Create a reusable human-in-the-loop process that lets an LLM collect, challenge, and synthesize research while authorized humans control scope, evidence promotion, experiments, theory promotion, and adoption. Implement the process as concise Codex skills, integrate it into this workspace, validate the skills independently, and then use it to continue the currently authorized GAR evidence-integration action.

# Context

Treat `CURRENT_STATE.md`, `research/NEXT_ACTION-001.md`, the research stage gates, frozen evidence ledgers, and EVAL-006 records as canonical. Stage 1 remains open because GAR introduced a material carbon-aware routing mechanism. No experiment or scheduler is active.

# Success criteria

1. Create three modular global skills under `/Users/tedahn/.codex/skills`: one for human research gates, one for bounded evidence-context engineering, and one for evaluable research-prompt design.
2. Give every skill valid YAML frontmatter, concise imperative instructions, matching `agents/openai.yaml`, explicit authority boundaries, and only resources that materially improve repeated execution.
3. Define a workspace process with named human roles, decision rights, gate inputs and outputs, evidence states, context-pack schema, prompt contract, escalation rules, audit trail, expiry/refresh rules, and stop conditions.
4. Forward-test each skill independently on a realistic task without leaking intended answers; repair material failures before adoption.
5. Instantiate the process for the current GAR action, then continue only the bounded public-source work authorized by `research/NEXT_ACTION-001.md`.

# Constraints

- Human decisions govern evidence promotion, theory promotion, experiment activation, and production adoption; model output is always provisional until the applicable gate is approved.
- Do not request hidden chain-of-thought. Require concise rationale, evidence, uncertainty, and verification instead.
- Do not assume dynamic routing is superior. Preserve single-model, static-router, and dynamic-router comparators plus negative evidence.
- Do not access private data, contact vendors, purchase access, activate a scheduler, rebaseline EVAL-006, run a scientific experiment, or make a production change.
- Preserve existing user work and frozen records. Use explicit supersession rather than silent overwrite.
- Continue GAR work within the current six-open or 60-minute public-source budget and stop on any material new method or measured-outcome category.

# Output

Persist the three validated global skill folders, the workspace human-in-the-loop workflow, a current gate record and bounded context pack, the GAR continuation snapshot and source-backed ledger changes, and updated navigation/state files when warranted.

# Validation

Run `quick_validate.py` for every skill, inspect forward-test results, run the workspace validator, CSV/cross-reference checks, `git diff --check`, and the EVAL-006 validator. Do not repair expected frozen-ledger hash drift by changing its manifest.
