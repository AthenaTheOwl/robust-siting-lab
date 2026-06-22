from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from robust_siting_lab.model import load_instance, solve_instance
from robust_siting_lab.scoring import compute_regret


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INSTANCE = ROOT / "benchmarks" / "toy_public.json"
DEFAULT_RESULT = ROOT / "results" / "toy_public.json"
DEFAULT_REPORT = ROOT / "reports" / "toy_public.jsonl"


def _write_outputs(instance_path: Path, result_path: Path, report_path: Path) -> dict:
    instance = load_instance(instance_path)
    solution = solve_instance(instance)
    regret = compute_regret(solution)
    payload = {"solution": solution, "regret": regret}
    result_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(json.dumps(regret, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def _validate(_args: argparse.Namespace) -> int:
    required = [
        ROOT / "PRODUCT_BRIEF.md",
        ROOT / "SYSTEM_MAP.md",
        ROOT / "STATUS.md",
        ROOT / "README.md",
        ROOT / "pyproject.toml",
        ROOT / "benchmarks" / "schema.json",
        DEFAULT_INSTANCE,
    ]
    missing = [path.as_posix() for path in required if not path.exists()]
    if missing:
        raise SystemExit("missing required files: " + ", ".join(missing))
    payload = _write_outputs(DEFAULT_INSTANCE, DEFAULT_RESULT, DEFAULT_REPORT)
    if payload["regret"]["announced_regret"] < 0:
        raise SystemExit("announced_regret must be non-negative")
    for line in DEFAULT_REPORT.read_text(encoding="utf-8").splitlines():
        json.loads(line)
    print(
        "OK "
        f"instance={payload['solution']['instance_id']} "
        f"selected={payload['solution']['selected_site']} "
        f"announced_regret={payload['regret']['announced_regret']}"
    )
    return 0


def _solve(args: argparse.Namespace) -> int:
    payload = _write_outputs(Path(args.instance), Path(args.out), DEFAULT_REPORT)
    print(json.dumps(payload["solution"], indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="robust_siting_lab")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="validate the bundled v0.1 artifact")
    validate.set_defaults(func=_validate)
    solve = sub.add_parser("solve", help="solve an instance")
    solve.add_argument("--instance", default=str(DEFAULT_INSTANCE))
    solve.add_argument("--out", default=str(DEFAULT_RESULT))
    solve.set_defaults(func=_solve)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
