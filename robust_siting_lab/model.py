"""Small deterministic siting model for the v0.1 benchmark."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CapexPlan:
    scenario_id: str
    queue_projects: int


@dataclass(frozen=True)
class FactorScore:
    name: str
    score: float


def load_instance(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def site_expected_cost(site: dict[str, Any], weights: dict[str, float]) -> float:
    return (
        site["capex_billion"] * weights["capex"]
        + site["grid_delay_risk"] * weights["grid_delay"]
        + site["water_shortfall_risk"] * weights["water_shortfall"]
        + site["silicon_delay_risk"] * weights["silicon_delay"]
    )


def solve_instance(instance: dict[str, Any]) -> dict[str, Any]:
    weights = instance["cost_weights"]
    scored = [
        {
            "site_id": site["site_id"],
            "expected_cost": round(site_expected_cost(site, weights), 6),
        }
        for site in instance["candidate_sites"]
    ]
    scored.sort(key=lambda row: (row["expected_cost"], row["site_id"]))
    selected = scored[0]
    announced_site = instance["announced_choice"]["site_id"]
    announced = next(row for row in scored if row["site_id"] == announced_site)
    return {
        "instance_id": instance["instance_id"],
        "selected_site": selected["site_id"],
        "selected_expected_cost": selected["expected_cost"],
        "announced_site": announced["site_id"],
        "announced_expected_cost": announced["expected_cost"],
        "scored_sites": scored,
    }


def rank_constraints(plan: CapexPlan) -> list[FactorScore]:
    return [
        FactorScore("grid-delay", min(1.0, plan.queue_projects / 10.0)),
        FactorScore("water-shortfall", 0.42),
        FactorScore("silicon-delay", 0.37),
    ]
