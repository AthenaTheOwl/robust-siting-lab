# Spec 0002 requirements

## R-RST-002-001 - default validation

`python -m robust_siting_lab validate` must run with no flags and validate the
checked toy benchmark, result file, and JSONL report row.

## R-RST-002-002 - toy benchmark

The v0.1 repo must include `benchmarks/toy_public.json` with at least three
candidate sites and public-source-shaped citation URLs.

## R-RST-002-003 - regret report

The solver must write a result containing selected site, announced site,
announced regret, and optimizer regret versus best.
