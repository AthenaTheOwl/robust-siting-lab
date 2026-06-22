from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    json.loads(Path("benchmarks/schema.json").read_text(encoding="utf-8"))
    json.loads(Path("benchmarks/toy_public.json").read_text(encoding="utf-8"))
    print("validate_schemas OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
