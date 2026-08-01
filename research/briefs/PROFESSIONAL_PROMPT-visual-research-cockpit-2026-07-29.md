# Professional prompt — visual research cockpit

Role: Design and implement an evidence-governed visual research cockpit for the OmniRouting Research Observatory.

# Goal

Create an in-conversation interactive visual that makes the current research program legible at a glance: cumulative research-run growth, the active discovery gate, the canonical discovery and theory/test workflows, method-to-outcome coverage, controller-evaluation status, key product-status decisions, and the single next action.

# Context

Use the canonical workspace state as of 2026-07-29 America/Chicago, especially `CURRENT_STATE.md`, `research/NEXT_ACTION-001.md`, the current CSV ledgers, `research/workflows/CONTINUOUS_THEORY_AND_TEST_WORKFLOW.md`, `research/snapshots/2026-07-29-independent-discovery-and-contradiction-pass.md`, and `research/validation/eval-006/FINAL_REPORT.md`. Treat current validator output as authoritative for present artifact integrity.

# Success criteria

- Show the pass-1 baseline and net-new pass-2 records on one explicitly labeled inventory-count scale.
- Separate the active Stage-1 discovery/consolidation lane from the drafted but inactive theory/experiment lane with a visible activation barrier.
- Show all 16 methodology families, their evidence state, and their recorded outcome/counterevidence coverage; expose the two outcomes without a method ID as unmapped evidence.
- Let the reader select a method and inspect its linked outcome records without implying a cross-system ranking.
- Separate protocol checks, synthetic controller coverage, scientific conclusions, and activation readiness.
- Keep current blockers visible: Stage 1 is open, EVAL-006 still requires human review and an uninterrupted rerun, and the current EVAL-006 integrity check fails because five scientific-ledger hashes changed.
- Work at conversation width and reflow cleanly to 320 px with semantic, keyboard-accessible controls and text-plus-color status encoding.

# Constraints

- Do not combine incompatible workloads, baselines, model pools, metrics, units, or time windows.
- Label counts as inventory, outcome records as experimental evidence, research priority as priority rather than endorsement, and controller checks as smoke tests rather than scientific or production validation.
- Do not claim an independent replication, completed Stripe–OpenRouter acquisition, active scheduler, activated experiment, or saturated Stage 1.
- Keep all data inline; do not fetch external or workspace resources at runtime.

# Output

Produce one focused HTML fragment in the thread visualization directory. Include only necessary labels, legends, values, status text, and accessible descriptions.

# Validation

Read the fragment back; reject escaped markup, undefined JavaScript identifiers, missing queried elements, inaccessible controls, overflow at narrow width, or interactions that do not update the selected method. Run the workspace validator and the EVAL-006 validator, and display their current states without rewriting the research ledgers.
