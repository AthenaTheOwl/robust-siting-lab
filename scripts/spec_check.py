from __future__ import annotations

from pathlib import Path


def main() -> int:
    required = [
        "specs/0002-design/requirements.md",
        "specs/0002-design/design.md",
        "specs/0002-design/tasks.md",
        "specs/0002-design/acceptance.md",
    ]
    missing = [path for path in required if not Path(path).exists()]
    if missing:
        raise SystemExit("missing spec files: " + ", ".join(missing))
    print("spec_check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
