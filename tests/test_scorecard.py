from __future__ import annotations

import json
from numbers import Real
from pathlib import Path
from tempfile import TemporaryDirectory

from robust_siting_lab.model import load_instance, solve_instance
from robust_siting_lab.scorecard import DEFAULT_INSTANCE, run


def _read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_scorecard_rows_cover_candidates_and_regret_contract() -> None:
    with TemporaryDirectory(prefix=".scorecard-test-", dir=Path("reports")) as tmp_dir:
        out_path = Path(tmp_dir) / "scorecard.jsonl"
        rows = run(report_path=out_path, emit_summary=False)
        instance = load_instance(DEFAULT_INSTANCE)
        candidate_sites = {site["site_id"] for site in instance["candidate_sites"]}
        optimal_site = solve_instance(instance)["selected_site"]

        assert len(rows) == len(instance["candidate_sites"])
        assert {row["announced_site"] for row in rows} == candidate_sites
        assert _read_jsonl(out_path) == rows
        for row in rows:
            assert "announced_site" in row
            assert "announced_regret" in row
            for regret_key in ("announced_regret", "optimizer_regret_vs_best"):
                assert isinstance(row[regret_key], Real)
                assert not isinstance(row[regret_key], bool)
                assert row[regret_key] >= 0

        optimal_rows = [row for row in rows if row["announced_site"] == optimal_site]
        assert len(optimal_rows) == 1
        assert optimal_rows[0]["announced_regret"] == 0.0


def test_scorecard_output_is_byte_stable() -> None:
    with TemporaryDirectory(prefix=".scorecard-test-", dir=Path("reports")) as tmp_dir:
        first_path = Path(tmp_dir) / "first.jsonl"
        second_path = Path(tmp_dir) / "second.jsonl"

        run(report_path=first_path, emit_summary=False)
        run(report_path=second_path, emit_summary=False)

        assert first_path.read_bytes() == second_path.read_bytes()
