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


def test_optimizer_regret_is_gap_between_selected_and_best() -> None:
    # The selected site's cost minus the cheapest scored site's cost, computed
    # from scored_sites rather than assumed to be zero.
    solution = {
        "instance_id": "synthetic",
        "selected_site": "b",
        "selected_expected_cost": 9.6,
        "announced_site": "c",
        "announced_expected_cost": 9.7,
        "scored_sites": [
            {"site_id": "a", "expected_cost": 9.474},
            {"site_id": "b", "expected_cost": 9.6},
            {"site_id": "c", "expected_cost": 9.7},
        ],
    }
    regret = compute_regret(solution)
    assert regret["optimizer_regret_vs_best"] == 0.126
    assert regret["announced_regret"] == 0.1


def test_optimizer_regret_on_toy_instance_matches_cost_gap() -> None:
    solution = solve_instance(load_instance(Path("benchmarks/toy_public.json")))
    best = min(row["expected_cost"] for row in solution["scored_sites"])
    regret = compute_regret(solution)
    assert regret["optimizer_regret_vs_best"] == round(
        solution["selected_expected_cost"] - best, 6
    )


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
