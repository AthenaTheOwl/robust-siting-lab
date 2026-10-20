"""Regret scoring and report helpers."""

from __future__ import annotations

import math

from robust_siting_lab.model import site_expected_cost, solve_instance


def compute_regret(solution: dict) -> dict:
    """Announced-choice regret and optimizer regret for one solved instance.

    optimizer_regret_vs_best is the selected site's cost minus the lowest
    scored cost. solve_instance is an exhaustive deterministic screen that
    always selects that lowest cost, so for any solver output this field is
    0.0 by construction: it is an internal consistency check, not a measured
    regret or a bound. The spec-0001 R-RST-007 quantity (regret against the
    perfect-foresight per-scenario optimum) needs scenarios, which v0.1 does
    not model. The field is kept because R-RST-002-003 lists it.
    """
    announced_regret = round(
        solution["announced_expected_cost"] - solution["selected_expected_cost"], 6
    )
    best_expected_cost = min(row["expected_cost"] for row in solution["scored_sites"])
    optimizer_regret_vs_best = round(
        solution["selected_expected_cost"] - best_expected_cost, 6
    )
    return {
        "instance_id": solution["instance_id"],
        "selected_site": solution["selected_site"],
        "announced_site": solution["announced_site"],
        "announced_regret": announced_regret,
        "optimizer_regret_vs_best": optimizer_regret_vs_best,
    }


# Risk weights are scaled together; the capex weight stays fixed so the scale
# reads as "how much the three risk proxies count relative to capex".
RISK_WEIGHT_KEYS = ("grid_delay", "water_shortfall", "silicon_delay")
SENSITIVITY_SCALES = (0.5, 0.75, 1.0, 1.25, 1.5)


def scale_risk_weights(weights: dict, scale: float) -> dict:
    return {
        key: value * scale if key in RISK_WEIGHT_KEYS else value
        for key, value in weights.items()
    }


def announced_optimal_scale_range(instance: dict) -> list | None:
    """Risk-weight scales k >= 0 at which the announced site ties or beats every other site.

    Each site's cost is capex_part + k * risk_part, so the announced site is
    optimal on an interval of k. Returns [low, high] (high is None when
    unbounded), or None when no non-negative scale makes it optimal.
    """
    weights = instance["cost_weights"]
    capex_only = {**weights, **{key: 0.0 for key in RISK_WEIGHT_KEYS}}
    risk_only = {**weights, "capex": 0.0}
    parts = {
        site["site_id"]: (
            site_expected_cost(site, capex_only),
            site_expected_cost(site, risk_only),
        )
        for site in instance["candidate_sites"]
    }
    announced_capex, announced_risk = parts[instance["announced_choice"]["site_id"]]
    low, high = 0.0, float("inf")
    for site_id, (capex, risk) in parts.items():
        if site_id == instance["announced_choice"]["site_id"]:
            continue
        # announced optimal vs this site iff capex_gap <= k * risk_gap
        capex_gap = announced_capex - capex
        risk_gap = risk - announced_risk
        if math.isclose(risk_gap, 0.0, abs_tol=1e-9):
            # equal weighted risk (up to float noise): the scale cannot help
            if capex_gap > 1e-9:
                return None
        elif risk_gap > 0:
            low = max(low, capex_gap / risk_gap)
        else:
            high = min(high, capex_gap / risk_gap)
    if low > high:
        return None
    return [round(low, 6), None if high == float("inf") else round(high, 6)]


def weight_sensitivity(instance: dict, scales: tuple = SENSITIVITY_SCALES) -> dict:
    """Announced regret when the hand-set risk weights are scaled up or down."""
    grid = []
    for scale in scales:
        scaled = {**instance, "cost_weights": scale_risk_weights(instance["cost_weights"], scale)}
        solution = solve_instance(scaled)
        regret = compute_regret(solution)
        grid.append(
            {
                "risk_weight_scale": scale,
                "selected_site": solution["selected_site"],
                "announced_regret": regret["announced_regret"],
                # undefined when the cheapest site costs 0
                "announced_regret_pct": None
                if solution["selected_expected_cost"] == 0
                else round(
                    100 * regret["announced_regret"] / solution["selected_expected_cost"], 6
                ),
            }
        )
    return {
        "scaled_weights": list(RISK_WEIGHT_KEYS),
        "fixed_weights": ["capex"],
        "announced_optimal_scale_range": announced_optimal_scale_range(instance),
        "grid": grid,
    }
