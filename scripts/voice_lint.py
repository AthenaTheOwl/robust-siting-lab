from __future__ import annotations

from pathlib import Path

BANNED = ("best-in-class", "synergy", "leverage")


def main() -> int:
    failures = []
    for path in [Path("README.md"), Path("PRODUCT_BRIEF.md"), Path("STATUS.md")]:
        text = path.read_text(encoding="utf-8").lower()
        for banned in BANNED:
            if banned in text:
                failures.append(f"{path}: banned word {banned}")
    if failures:
        raise SystemExit("\n".join(failures))
    print("voice_lint OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
