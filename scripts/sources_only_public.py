from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    data = json.loads(Path("benchmarks/toy_public.json").read_text(encoding="utf-8"))
    bad = [
        value
        for value in data.get("citations", {}).values()
        if not isinstance(value, str) or not value.startswith("https://")
    ]
    if bad:
        raise SystemExit(f"non-public citation values: {bad}")
    print("sources_only_public OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
