"""Regret scoring and report helpers."""

from __future__ import annotations


def compute_regret(solution: dict) -> dict:
    announced_regret = round(
        solution["announced_expected_cost"] - solution["selected_expected_cost"], 6
    )
    return {
        "instance_id": solution["instance_id"],
        "selected_site": solution["selected_site"],
        "announced_site": solution["announced_site"],
        "announced_regret": announced_regret,
        "optimizer_regret_vs_best": 0.0,
    }
