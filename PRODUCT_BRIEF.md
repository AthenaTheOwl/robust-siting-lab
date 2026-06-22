# Product brief

Robust Siting Lab v0.1 is a local benchmark for comparing public data-center
siting choices against a simple joint-risk optimizer. The first user action is:

```powershell
python -m robust_siting_lab validate
```

The command validates the toy benchmark, runs the deterministic solver, checks
regret output, and confirms the checked report row is readable.

## User

- Infrastructure analysts comparing grid, water, and silicon constraints in one
  decision frame.
- Optimization researchers who need a small reproducible benchmark before
  scaling to larger public instances.
- Portfolio operators who want a report row they can diff in git.

## v0.1 artifact

- `benchmarks/toy_public.json`
- `reports/toy_public.jsonl`
- `results/toy_public.json`

## Quality bar

- No network access at gate time.
- Every numeric field carries a public-source-shaped URL in `citations`.
- The solver's regret against the announced choice is non-negative and reported.
