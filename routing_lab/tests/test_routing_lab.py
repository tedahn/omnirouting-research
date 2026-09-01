from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from routing_lab.cli import main as cli_main
from routing_lab.context import build_context, capability_map
from routing_lab.evaluator import evaluate_policy
from routing_lab.optimizer import apply_proposal, optimize_policy
from routing_lab.router import route_request, simulate_workflow
from routing_lab.store import LabStore, StoreError


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class RoutingLabTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        workspace = root / "workspace"
        shutil.copytree(PACKAGE_ROOT / "workspace", workspace)
        self.store = LabStore(workspace=workspace, runtime=root / "runtime")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _decision(self, case_id: str) -> dict:
        case = self.store.get("case", case_id, suite="development")
        policy = self.store.get("policy", "adaptive-score-v1")
        return route_request(
            self.store,
            case["request"],
            policy=policy,
            predictions=case["predictions"],
            audit=False,
        )

    def test_workspace_contracts_validate(self) -> None:
        result = self.store.validate_all()
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(
            result["counts"],
            {"model": 5, "policy": 2, "workflow": 1, "objective": 3, "case": 12},
        )

    def test_atomic_crud_is_complete(self) -> None:
        model = deepcopy(self.store.get("model", "fast-general"))
        model["id"] = "temporary-model"
        created = self.store.put("model", model, actor="test")
        self.assertEqual(created["operation"], "create")
        self.assertEqual(self.store.get("model", "temporary-model")["provider"], "fixture")
        model["provider"] = "updated-fixture"
        updated = self.store.put("model", model, actor="test")
        self.assertEqual(updated["operation"], "update")
        self.assertEqual(self.store.get("model", "temporary-model")["provider"], "updated-fixture")
        deleted = self.store.delete("model", "temporary-model", actor="test")
        self.assertEqual(deleted["operation"], "delete")
        with self.assertRaises(StoreError):
            self.store.get("model", "temporary-model")

    def test_confirmation_cases_are_mutation_protected(self) -> None:
        case = self.store.get("case", "confirm-reasoning", suite="confirmation")
        with self.assertRaisesRegex(StoreError, "mutation-protected"):
            self.store.put("case", case, suite="confirmation", actor="test")
        with self.assertRaisesRegex(StoreError, "mutation-protected"):
            self.store.delete("case", case["id"], suite="confirmation", actor="test")

    def test_active_policy_and_objective_are_not_raw_crud_targets(self) -> None:
        policy = self.store.active_policy()
        policy["description"] += " unsafe in-place edit"
        with self.assertRaisesRegex(StoreError, "cannot be changed through raw CRUD"):
            self.store.put("policy", policy, actor="test")
        with self.assertRaisesRegex(StoreError, "cannot be changed through raw CRUD"):
            self.store.delete("objective", self.store.state()["active_objective"], actor="test")

    def test_router_selects_fast_model_for_simple_case(self) -> None:
        decision = self._decision("dev-fast-extraction")
        self.assertEqual(decision["selected_target"], "fast-general")
        self.assertFalse(decision["abstained"])

    def test_router_selects_deep_model_for_high_risk_case(self) -> None:
        decision = self._decision("dev-hard-reasoning")
        self.assertEqual(decision["selected_target"], "deep-reasoner")
        balanced = next(item for item in decision["candidates"] if item["target_id"] == "balanced-general")
        self.assertIn("below_risk_quality_floor", balanced["exclusion_reasons"])

    def test_router_routes_agent_kind_targets(self) -> None:
        self.assertEqual(self._decision("dev-agent-triage")["selected_target"], "quick-agent")
        self.assertEqual(self._decision("dev-agent-planning")["selected_target"], "workflow-agent")

    def test_policy_normalization_preserves_efficiency_without_request_budgets(self) -> None:
        decision = route_request(
            self.store,
            {
                "id": "unbudgeted-simple-call",
                "route_kind": "model",
                "required_capabilities": ["text"],
                "complexity": 0.1,
                "risk": "low",
            },
            policy=self.store.get("policy", "adaptive-score-v1"),
            audit=False,
        )
        self.assertEqual(decision["selected_target"], "fast-general")
        fast = next(item for item in decision["candidates"] if item["target_id"] == "fast-general")
        balanced = next(
            item for item in decision["candidates"] if item["target_id"] == "balanced-general"
        )
        self.assertGreater(fast["score"], balanced["score"])

    def test_workflow_routes_each_stage_with_one_primitive(self) -> None:
        workflow = self.store.get("workflow", "research-assist-v1")
        result = simulate_workflow(
            self.store,
            workflow,
            {"id": "test-workflow", "complexity": 0.5, "risk": "medium"},
            policy=self.store.get("policy", "adaptive-score-v1"),
            audit=False,
        )
        self.assertEqual(result["status"], "completed")
        self.assertEqual([stage["stage_id"] for stage in result["stages"]], ["triage", "plan", "execute", "review"])
        self.assertEqual(result["stages"][0]["decision"]["route_kind"], "model")
        self.assertEqual(result["stages"][1]["decision"]["route_kind"], "agent")

    def test_adaptive_policy_improves_fixture_success_without_hard_regression(self) -> None:
        baseline = evaluate_policy(
            self.store,
            self.store.get("policy", "baseline-static-v1"),
            suite="development",
        )
        adaptive = evaluate_policy(
            self.store,
            self.store.get("policy", "adaptive-score-v1"),
            suite="development",
        )
        self.assertGreater(
            adaptive["metrics"]["task_success_rate"],
            baseline["metrics"]["task_success_rate"],
        )
        self.assertEqual(adaptive["metrics"]["hard_violation_rate"], 0)
        self.assertIn("brier_score", adaptive["metrics"])
        self.assertIn("latency_p95_ms", adaptive["metrics"])
        self.assertIn("mean_oracle_regret", adaptive["metrics"])
        self.assertIn("mean_cost_budget_utilization", adaptive["metrics"])
        self.assertEqual(adaptive["objective_id"], "balanced-objective-v1")

    def test_partitioned_reports_hash_the_exact_evaluated_subset(self) -> None:
        policy = self.store.get("policy", "adaptive-score-v1")
        train = evaluate_policy(
            self.store,
            policy,
            suite="development",
            partitions={"train"},
        )
        validation = evaluate_policy(
            self.store,
            policy,
            suite="development",
            partitions={"validation"},
        )
        self.assertEqual(train["dataset_sha256"], validation["dataset_sha256"])
        self.assertNotEqual(
            train["evaluated_subset_sha256"], validation["evaluated_subset_sha256"]
        )

    def test_optimizer_proposes_without_activation_or_confirmation_access(self) -> None:
        active_before = self.store.state()["active_policy"]
        confirmation_hash = self.store.dataset_hash("confirmation")
        proposal = optimize_policy(
            self.store,
            self.store.get("policy", "baseline-static-v1"),
            suite="development",
        )
        self.assertTrue(proposal["promotion_allowed"])
        self.assertGreater(proposal["validation_objective_improvement"], 0)
        self.assertFalse(proposal["search"]["confirmation_accessed"])
        self.assertEqual(self.store.dataset_hash("confirmation"), confirmation_hash)
        self.assertEqual(self.store.state()["active_policy"], active_before)

    def test_optimizer_rejects_confirmation_suite(self) -> None:
        with self.assertRaisesRegex(StoreError, "forbidden"):
            optimize_policy(
                self.store,
                self.store.get("policy", "baseline-static-v1"),
                suite="confirmation",
            )

    def test_proposal_application_requires_human_and_rechecks_hashes(self) -> None:
        proposal = optimize_policy(
            self.store,
            self.store.get("policy", "baseline-static-v1"),
        )
        with self.assertRaisesRegex(StoreError, "human reviewer"):
            apply_proposal(self.store, proposal["id"], approved_by="agent")
        applied = apply_proposal(self.store, proposal["id"], approved_by="Test Human")
        self.assertEqual(applied["status"], "applied_to_simulation")
        self.assertEqual(self.store.state()["active_policy"], applied["candidate_policy"]["id"])
        self.assertEqual(self.store.state()["mode"], "simulation_only")

    def test_stale_proposal_cannot_be_applied(self) -> None:
        proposal = optimize_policy(
            self.store,
            self.store.get("policy", "baseline-static-v1"),
        )
        case = self.store.get("case", "dev-fast-extraction", suite="development")
        case["description"] += " Changed after proposal."
        self.store.put("case", case, suite="development", actor="test")
        with self.assertRaisesRegex(StoreError, "dataset changed"):
            apply_proposal(self.store, proposal["id"], approved_by="Test Human")

    def test_dynamic_context_and_capability_parity(self) -> None:
        context = build_context(self.store)
        self.assertEqual(context["mode"], "simulation_only")
        self.assertEqual(len(context["models"]), 5)
        self.assertEqual(len(context["objectives"]), 3)
        actions = capability_map()["actions"]
        action_text = " ".join(action["action"] for action in actions).lower()
        for operation in ("create", "read", "update", "delete"):
            self.assertIn(operation, action_text)

    def test_json_cli_validation_surface(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exitcode = cli_main(
                [
                    "--workspace",
                    str(self.store.workspace),
                    "--runtime",
                    str(self.store.runtime),
                    "validate",
                ]
            )
        self.assertEqual(exitcode, 0)
        payload = json.loads(stdout.getvalue())
        self.assertTrue(payload["ok"])
        self.assertTrue(payload["result"]["valid"])

    def test_json_cli_confirmation_read_requires_explicit_flag(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        arguments = [
            "--workspace",
            str(self.store.workspace),
            "--runtime",
            str(self.store.runtime),
            "resource",
            "list",
            "case",
            "--suite",
            "confirmation",
        ]
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            blocked = cli_main(arguments)
        self.assertEqual(blocked, 2)
        self.assertIn("requires --allow-confirmation", stderr.getvalue())
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            allowed = cli_main(arguments + ["--allow-confirmation"])
        self.assertEqual(allowed, 0)
        self.assertEqual(len(json.loads(stdout.getvalue())["result"]["resources"]), 4)


if __name__ == "__main__":
    unittest.main()
