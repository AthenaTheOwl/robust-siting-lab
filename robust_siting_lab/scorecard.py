from __future__ import annotations

import json
import sys
from numbers import Real
from pathlib import Path
from typing import Any

from robust_siting_lab.model import load_instance, solve_instance
from robust_siting_lab.scoring import compute_regret


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INSTANCE = ROOT / "benchmarks" / "toy_public.json"
DEFAULT_REPORT = ROOT / "reports" / "scorecard.jsonl"


class ScorecardError(Exception):
    """Typed scorecard failure for clean command-line exits."""


def _candidate_site_ids(instance: dict[str, Any]) -> list[str]:
    try:
        candidate_sites = instance["candidate_sites"]
        site_ids = [site["site_id"] for site in candidate_sites]
    except KeyError as exc:
        raise ScorecardError(f"instance is missing required key: {exc.args[0]}") from exc
    except TypeError as exc:
        raise ScorecardError("instance candidate_sites must be a list of site records") from exc
    if not site_ids:
        raise ScorecardError("instance candidate_sites must contain at least one site")
    return site_ids


def _instance_with_announced_site(instance: dict[str, Any], site_id: str) -> dict[str, Any]:
    announced_choice = dict(instance.get("announced_choice", {}))
    announced_choice["site_id"] = site_id
    return {**instance, "announced_choice": announced_choice}


def build_rows(instance: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for site_id in _candidate_site_ids(instance):
        solution = solve_instance(_instance_with_announced_site(instance, site_id))
        regret = compute_regret(solution)
        rows.append(
            {
                "announced_expected_cost": solution["announced_expected_cost"],
                "announced_regret": regret["announced_regret"],
                "announced_site": regret["announced_site"],
                "instance_id": regret["instance_id"],
                "optimizer_regret_vs_best": regret["optimizer_regret_vs_best"],
                "selected_site": regret["selected_site"],
            }
        )
    return rows


def _write_jsonl(rows: list[dict[str, Any]], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _lowest_regret_site(rows: list[dict[str, Any]]) -> str:
    row = min(rows, key=lambda item: (item["announced_regret"], item["announced_site"]))
    regret = row["announced_regret"]
    if not isinstance(regret, Real) or isinstance(regret, bool):
        raise ScorecardError("announced_regret must be a real number")
    return str(row["announced_site"])


def run(
    instance_path: Path = DEFAULT_INSTANCE,
    report_path: Path = DEFAULT_REPORT,
    *,
    emit_summary: bool = True,
) -> list[dict[str, Any]]:
    try:
        instance = load_instance(instance_path)
        rows = build_rows(instance)
        _write_jsonl(rows, report_path)
        lowest_site = _lowest_regret_site(rows)
    except OSError as exc:
        raise ScorecardError(f"cannot read or write scorecard files: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ScorecardError(f"instance {instance_path} is not valid JSON: {exc}") from exc
    except KeyError as exc:
        raise ScorecardError(f"engine output is missing required key: {exc.args[0]}") from exc
    except StopIteration as exc:
        raise ScorecardError("announced site was not found in scored sites") from exc

    if emit_summary:
        print(f"scorecard: wrote {len(rows)} rows; lowest announced_regret={lowest_site}")
    return rows


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args:
        print("ERROR[scorecard]: no arguments are supported", file=sys.stderr)
        return 2
    try:
        run()
    except ScorecardError as exc:
        print(f"ERROR[scorecard]: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR[scorecard]: unexpected failure: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
