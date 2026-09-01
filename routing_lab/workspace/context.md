# Routing lab context

This is a shared development workspace for humans and agents. It tests routing
mechanics with synthetic outcomes; it is not an active scientific experiment or
production router.

Current operating rules:

- Keep live provider calls disabled. Import measured outcomes as new cases only
  after their data boundary and provenance are approved elsewhere.
- Use `development` train and validation cases for policy search.
- Never tune on `confirmation`; the CLI protects mutation and the optimizer
  rejects that suite.
- Agents may create and edit sandbox resources. Optimizer output is a proposal,
  never an automatic activation.
- Applying a proposal requires a named human and changes only this local
  simulation state. Research promotion, online tests, and production adoption
  remain governed by the repository's existing gates.
- Record completion explicitly with `complete-task` and include verification
  artifacts as evidence.

Accumulated findings belong below this line. State whether each finding came
from a synthetic fixture, a measured run, or an inference.
