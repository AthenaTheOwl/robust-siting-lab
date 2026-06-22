"""Regret scoring and report helpers."""

from __future__ import annotations

import json
from pathlib import Path

from robust_siting_lab.model import FactorScore


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


def write_report(scores: list[FactorScore], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(score.__dict__, sort_keys=True) for score in scores) + "\n",
        encoding="utf-8",
    )
    return path
