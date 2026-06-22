from __future__ import annotations

from robust_siting_lab.cli import main


def test_validate_default_passes(capsys) -> None:
    assert main(["validate"]) == 0
    assert "OK instance=toy_public" in capsys.readouterr().out
