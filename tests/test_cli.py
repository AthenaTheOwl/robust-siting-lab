from __future__ import annotations

import pytest

from robust_siting_lab.cli import main


def test_validate_default_passes(capsys) -> None:
    assert main(["validate"]) == 0
    assert "OK instance=toy_public" in capsys.readouterr().out


def test_show_prints_ranked_result(capsys) -> None:
    assert main(["show"]) == 0
    out = capsys.readouterr().out
    # ranked table header + the optimal/announced rows + a regret headline
    assert "ranked by expected cost" in out
    assert "optimal" in out
    assert "announced" in out
    assert "lowest expected cost: ercot-west" in out
    assert "regret" in out


def test_solve_missing_instance_reports_clean_error(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["solve", "--instance", "does_not_exist.json"])
    # nonzero exit with an actionable message, not a traceback
    assert exc.value.code != 0
    message = str(exc.value.code)
    assert "does_not_exist.json" in message
