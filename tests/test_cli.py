from __future__ import annotations

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
