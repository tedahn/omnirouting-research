# Professional prompt — human decision agent council

Role: Human-AI research governance and decision-systems architect working inside the OmniRouting evidence observatory.

## Goal

Introduce a minimal set of reusable AI advisory agents and explicit human roles that reduce the effort required to move research through G0-G6 while preserving human accountability, separation of duties, and bounded authority. Apply the system immediately to the pending Agora integration decision.

## Context

- Stage 1 remains open after GAR integration and the Agora material-addition stop.
- `workflows/HUMAN_AI_RESEARCH_PROCESS.md` defines the existing G0-G6 ladder.
- `govern-human-ai-research` prohibits an LLM from approving its own evidence, theory, experiment, result, or adoption.
- `NEXT_ACTION-001.md` requires a new human decision before Agora integration.

## Success criteria

- Each advisory agent has a single purpose, human counterpart, gate coverage, required inputs, allowed and forbidden actions, output contract, and stop/escalation rule.
- Every consequential gate retains a named human decision owner; unassigned mandatory roles are visible blockers.
- The workflow presents one narrow decision at a time and supports `approve`, `approve_with_conditions`, `revise`, `reject`, `defer`, and `expire` without inferring approval from silence.
- Evidence challenge, methodology review, risk/authority review, independent evaluation, and decision recording remain separable.
- A reusable decision-packet template makes options, recommendation limits, dissent, reversal evidence, expiry, and the next bounded action explicit.
- A proposed Agora G0 record requests exactly one human decision and grants no authority until signed.

## Constraints

- Advisory agents may retrieve, normalize, challenge, calculate, draft, route, and record; they may not approve or sign human gates.
- Same-model review is not independent review.
- Do not authorize private data, paid retrieval, experiments, production actions, profiles, scheduling, theory promotion, or silent EVAL-006 rebaselining.
- Preserve the existing dirty working tree and all prior evidence.
- Prefer a small council over role proliferation; invoke only agents required by the current gate.

## Output

Create:

1. A council workflow and human responsibility matrix.
2. Reusable advisory-agent role cards.
3. A human decision-packet template.
4. A proposed `GATE-002` for bounded Agora public-source integration.
5. Updated workspace navigation and the current handoff.

## Validation

- Confirm no advisory role has approval authority.
- Confirm all G0-G6 decisions map to a human owner and required reviewer.
- Confirm GATE-002 remains `proposed` and asks one decision.
- Run `python3 scripts/validate_workspace.py` and `git diff --check`.
