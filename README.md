# Robust Siting Lab

Robust Siting Lab is a small public-source-shaped benchmark for joint grid,
water, and silicon siting risk. It asks one decision question: given a set of
candidate data-center sites and risk weights, which site has the lowest expected
cost, and how much regret does the announced choice carry?

## How to run

The first user action validates the bundled v0.1 artifact with no flags:

```powershell
python -m robust_siting_lab validate
```

To regenerate the checked result:

```powershell
python -m robust_siting_lab solve --instance benchmarks/toy_public.json --out results/toy_public.json
```

## What ships in v0.1

- `benchmarks/toy_public.json`: three-site toy benchmark with public-source-shaped citations.
- `benchmarks/schema.json`: benchmark shape.
- `robust_siting_lab/`: deterministic scoring and regret code.
- `results/toy_public.json`: checked solution.
- `reports/toy_public.jsonl`: one machine-readable report row.
- `PRODUCT_BRIEF.md`, `SYSTEM_MAP.md`, `STATUS.md`, and `specs/0002-design/`.

## What this is not

- Not a production siting recommendation.
- Not a live public-filing ingest.
- Not a commercial-solver benchmark.
- Not a forecast.

The next pass is to replace the toy fixture with reviewed public Meta and
Microsoft benchmark instances.

## License

MIT. See `LICENSE`.
