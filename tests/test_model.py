from __future__ import annotations

from pathlib import Path

from robust_siting_lab.model import load_instance, solve_instance
from robust_siting_lab.scoring import (
    announced_optimal_scale_range,
    compute_regret,
    scale_risk_weights,
    weight_sensitivity,
)


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


def test_optimizer_regret_is_zero_by_construction_for_solver_output() -> None:
    # solve_instance enumerates every site and selects the cheapest, so
    # selected minus best is 0.0 for any instance it solves. The field is a
    # consistency check, not a measured regret (R-RST-007 needs scenarios).
    base = load_instance(Path("benchmarks/toy_public.json"))
    for scale in (0.0, 0.25, 0.485, 1.0, 3.0):
        instance = {**base, "cost_weights": scale_risk_weights(base["cost_weights"], scale)}
        assert compute_regret(solve_instance(instance))["optimizer_regret_vs_best"] == 0.0


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


def test_announced_optimal_scale_range_on_toy_instance() -> None:
    # az-campus has the lowest capex, so it wins once the risk weights shrink
    # far enough: 7.9 + 1.786k <= 8.1 + 1.374k  ->  k <= 0.2 / 0.412.
    instance = load_instance(Path("benchmarks/toy_public.json"))
    assert announced_optimal_scale_range(instance) == [0.0, 0.485437]
    for scale, announced_wins in ((0.48, True), (0.49, False)):
        scaled = {**instance, "cost_weights": scale_risk_weights(instance["cost_weights"], scale)}
        assert (solve_instance(scaled)["selected_site"] == "az-campus") is announced_wins


def test_announced_optimal_scale_range_unbounded_and_empty() -> None:
    weights = {"capex": 1.0, "grid_delay": 1.0, "water_shortfall": 1.0, "silicon_delay": 1.0}

    def site(site_id, capex, risk):
        return {
            "site_id": site_id,
            "capex_billion": capex,
            "grid_delay_risk": risk,
            "water_shortfall_risk": 0.0,
            "silicon_delay_risk": 0.0,
        }

    low_risk_announced = {
        "candidate_sites": [site("a", 9.0, 0.1), site("b", 8.0, 0.6)],
        "cost_weights": weights,
        "announced_choice": {"site_id": "a"},
    }
    assert announced_optimal_scale_range(low_risk_announced) == [2.0, None]
    dominated_announced = {**low_risk_announced, "announced_choice": {"site_id": "c"}}
    dominated_announced["candidate_sites"] = [site("a", 8.0, 0.1), site("c", 9.0, 0.2)]
    assert announced_optimal_scale_range(dominated_announced) is None
    # same weighted risk as another site but higher capex: no scale helps
    equal_risk_announced = {**low_risk_announced, "announced_choice": {"site_id": "c"}}
    equal_risk_announced["candidate_sites"] = [site("a", 8.0, 0.2), site("c", 9.0, 0.2)]
    assert announced_optimal_scale_range(equal_risk_announced) is None


def test_announced_optimal_scale_range_tolerates_float_ties() -> None:
    # 0.1 + 0.2 and 0.3 are equal weighted risk but differ by ~5e-17 as floats.
    weights = {"capex": 1.0, "grid_delay": 1.0, "water_shortfall": 1.0, "silicon_delay": 1.0}
    sites = [
        {"site_id": "a", "capex_billion": 8.0, "grid_delay_risk": 0.1,
         "water_shortfall_risk": 0.2, "silicon_delay_risk": 0.0},
        {"site_id": "b", "capex_billion": 9.0, "grid_delay_risk": 0.3,
         "water_shortfall_risk": 0.0, "silicon_delay_risk": 0.0},
    ]
    instance = {"candidate_sites": sites, "cost_weights": weights}
    assert announced_optimal_scale_range({**instance, "announced_choice": {"site_id": "a"}}) == [0.0, None]
    assert announced_optimal_scale_range({**instance, "announced_choice": {"site_id": "b"}}) is None


def test_weight_sensitivity_handles_zero_cost_cheapest_site() -> None:
    zero = {"capex_billion": 0.0, "grid_delay_risk": 0.0,
            "water_shortfall_risk": 0.0, "silicon_delay_risk": 0.0}
    instance = {
        "instance_id": "zero",
        "candidate_sites": [{**zero, "site_id": "a"}, {**zero, "site_id": "b"}],
        "cost_weights": {"capex": 1.0, "grid_delay": 1.0, "water_shortfall": 1.0, "silicon_delay": 1.0},
        "announced_choice": {"site_id": "b"},
    }
    grid = weight_sensitivity(instance)["grid"]
    assert all(row["announced_regret_pct"] is None for row in grid)


def test_weight_sensitivity_grid_is_pinned() -> None:
    instance = load_instance(Path("benchmarks/toy_public.json"))
    sensitivity = weight_sensitivity(instance)
    assert sensitivity["fixed_weights"] == ["capex"]
    assert [
        (row["risk_weight_scale"], row["selected_site"], row["announced_regret"])
        for row in sensitivity["grid"]
    ] == [
        (0.5, "ercot-west", 0.006),
        (0.75, "ercot-west", 0.109),
        (1.0, "ercot-west", 0.212),
        (1.25, "ercot-west", 0.315),
        (1.5, "pjm-west", 0.485),
    ]
    # the unscaled row reproduces the headline regret and its percentage
    unscaled = sensitivity["grid"][2]
    assert unscaled["announced_regret"] == compute_regret(solve_instance(instance))["announced_regret"]
    assert round(unscaled["announced_regret_pct"], 1) == 2.2
    # pin the percentages exactly; the denominator is the cheapest site's cost
    assert [row["announced_regret_pct"] for row in sensitivity["grid"]] == [
        0.068283,
        1.193801,
        2.237703,
        3.208556,
        4.804835,
    ]
