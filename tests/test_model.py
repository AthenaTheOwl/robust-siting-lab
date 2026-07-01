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


def test_scored_costs_are_pinned() -> None:
    # Golden-master lock on the toy instance: pin the actual expected-cost
    # numbers so scrambling the factor weights fails even when the winner
    # (ercot-west) stays the same.
    solution = solve_instance(load_instance(Path("benchmarks/toy_public.json")))
    assert solution["scored_sites"] == [
        {"site_id": "ercot-west", "expected_cost": 9.474},
        {"site_id": "pjm-west", "expected_cost": 9.596},
        {"site_id": "az-campus", "expected_cost": 9.686},
    ]
    assert solution["selected_expected_cost"] == 9.474
    assert solution["announced_expected_cost"] == 9.686


def test_announced_regret_magnitude_is_pinned() -> None:
    # Pin the headline regret magnitude (9.686 - 9.474) so a mutation that
    # scales it cannot pass on a >= 0 check alone.
    regret = compute_regret(solve_instance(load_instance(Path("benchmarks/toy_public.json"))))
    assert regret["announced_regret"] == 0.212
