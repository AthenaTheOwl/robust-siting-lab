from __future__ import annotations

from pathlib import Path

from robust_siting_lab.model import load_instance, solve_instance
from robust_siting_lab.scoring import compute_regret


def test_solver_selects_lowest_expected_cost() -> None:
    solution = solve_instance(load_instance(Path("benchmarks/toy_public.json")))
    assert solution["selected_site"] == "ercot-west"
    assert solution["selected_expected_cost"] <= solution["announced_expected_cost"]


def test_regret_is_reported() -> None:
    regret = compute_regret(solve_instance(load_instance(Path("benchmarks/toy_public.json"))))
    assert regret["announced_regret"] >= 0
    assert regret["optimizer_regret_vs_best"] == 0.0
