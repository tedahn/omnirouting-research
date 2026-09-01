# OmniRouting agent routing lab

This is an agent-operable, simulation-first harness for testing how requests and
agentic workflow stages should route across model and agent targets. It gives
humans and agents the same JSON CLI, a shared file workspace, deterministic
fixtures, outcome-based evaluation, and a guarded offline optimization loop.

No dependency installation is required; Python 3.11+ is sufficient.

## Quick start

From the repository root:

```bash
python3 -m routing_lab validate
python3 -m routing_lab context
python3 -m routing_lab route --request routing_lab/examples/request.json
python3 -m routing_lab workflow research-assist-v1 \
  --input routing_lab/examples/workflow-input.json
```

Compare the static baseline with the adaptive policy:

```bash
python3 -m routing_lab evaluate --policy baseline-static-v1 \
  --objective balanced-objective-v1 --suite development
python3 -m routing_lab evaluate --policy adaptive-score-v1 \
  --objective balanced-objective-v1 --suite development
```

Generate—but do not activate—an optimized candidate:

```bash
python3 -m routing_lab optimize --base-policy baseline-static-v1 \
  --objective balanced-objective-v1 --suite development
python3 -m routing_lab proposal list
python3 -m routing_lab proposal show PROPOSAL_ID
```

Applying a proposal is intentionally separate and requires a named human:

```bash
python3 -m routing_lab proposal apply PROPOSAL_ID \
  --approved-by "Human reviewer name"
```

That approval changes only the local `simulation_only` active policy and
objective. The CLI records the approver name but does not authenticate identity.
It does not authorize confirmation-set access, a scientific claim, online
traffic, or production adoption.

## Atomic agent interface

All commands emit JSON and nonzero status on failure. Discover the current
contract with:

```bash
python3 -m routing_lab capabilities
python3 -m routing_lab resource list model
python3 -m routing_lab resource get policy adaptive-score-v1
```

Create or update any target, policy, objective, workflow, or case by passing a
JSON file to `resource put`. Delete is available with
`resource delete ... --yes`. Cases additionally take
`--suite development|confirmation`; confirmation reads, writes, and evaluation
require `--allow-confirmation`, and optimization rejects that suite entirely.

Agents should start from [AGENT_PROMPT.md](AGENT_PROMPT.md). The full rationale,
guardrails, and architecture checklist are in [ARCHITECTURE.md](ARCHITECTURE.md).

## Test

```bash
python3 -m unittest discover -s routing_lab/tests -v
python3 scripts/validate_workspace.py
git diff --check
```

The fixture metrics demonstrate harness behavior only. Replace or extend cases
with approved, provenance-bearing measurements before drawing conclusions about
real models or providers.
