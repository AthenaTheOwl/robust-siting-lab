# Status

## Current state

- v0.1 ships a toy public-source-shaped benchmark and deterministic solver.
- `python -m robust_siting_lab validate` runs with no flags.
- The checked result and JSONL report row are committed for review.

## Known limits

- The benchmark is synthetic and small; it is not a Meta or Microsoft public
  instance yet.
- The solver enumerates candidate sites instead of using Benders or L-shaped
  decomposition.
- Citation checks validate URL shape only; they do not fetch remote pages.

## Next feature queue

- Add `benchmarks/meta_2026_public.json` from reviewed public filings.
- Add `benchmarks/msft_2026_public.json` with the same schema.
- Replace enumeration with a decomposition module after the fixture expands.
- Add the arxiv-style paper draft once two public instances exist.
