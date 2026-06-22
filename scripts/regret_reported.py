from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    result = json.loads(Path("results/toy_public.json").read_text(encoding="utf-8"))
    if "announced_regret" not in result.get("regret", {}):
        raise SystemExit("missing announced_regret")
    print("regret_reported OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
