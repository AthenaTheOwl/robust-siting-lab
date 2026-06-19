# RobustSiting — Open Benchmark and Optimization Paper

A two-stage stochastic optimization solver plus an open benchmark
modeled on publicly disclosed Meta and Microsoft AI data-center
expansion plans. The benchmark asks one question: under joint
uncertainty across grid energization, water-rights allocation, and
silicon supply, what does the optimizer recommend, and how far is that
from the announced choice?

## What this is

Hyperscalers commit hundreds of billions of dollars per year to AI
data-center capex while treating grid, water, and silicon as siloed
axes. A four-to-five-year transformer lead time means siting decisions
made in 2026 lock in 2030 outcomes. The cost of a bad decision is in
the tens of billions per company.

RobustSiting is an open-source two-stage stochastic optimization model
of the joint problem, packaged with:

- A scenario library covering grid uncertainty (interconnection-queue
  survival), water-rights uncertainty (drought and basin-allocation
  scenarios), and silicon-allocation uncertainty (CoWoS, HBM, substrate
  bottlenecks)
- Two seed benchmark instances modeled on Meta 2026 public expansion
  filings and Microsoft 2026 public expansion filings
- A decomposition-based solver
- A regret-bound evaluation script
- An arxiv-shaped paper draft

The benchmark is the artifact. If you want to claim a better solver,
you publish your regret on the same instances.

## Status

v0 scaffold. No implementation yet — only the spec ledger and the file
layout below. First runnable code lands in spec 0002.

- [x] Repo scaffold + LICENSE + AGENTS.md
- [x] Spec 0001 (foundation) — requirements, design, tasks, acceptance
- [x] First-PR plan in `docs/first-pr.md`
- [ ] Benchmark instance schema
- [ ] First instance (Meta 2026 public)
- [ ] Two-stage stochastic model (small toy variant)
- [ ] Regret-bound evaluation harness
- [ ] arxiv paper draft

## How to run

Placeholder. The runnable solver lands in spec 0002. Intended shape:

```bash
uv sync
uv run robust-siting solve \
    --instance benchmarks/meta_2026_public.json \
    --scenarios 200 \
    --out results/meta_2026_public.json
uv run robust-siting regret \
    --instance benchmarks/meta_2026_public.json \
    --result results/meta_2026_public.json
```

Until spec 0002 lands, the only thing that runs is
`python -c "print('scaffold')"`.

## Layout

```
robust-siting-lab/
  README.md
  LICENSE
  AGENTS.md
  .gitignore
  specs/
    0001-foundation/
      requirements.md
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
```

Planned but not yet present:

```
  src/
    model/
      two_stage_stochastic.py
    scenarios/
      grid_uncertainty.py
      water_rights.py
      silicon_allocation.py
    solver/
      decomposition.py
    eval/
      regret_metrics.py
  benchmarks/
    meta_2026_public.json
    msft_2026_public.json
    schema.json
  paper/
    robust-siting.tex
  cli/
    main.py
  tests/
    fixtures/
  pyproject.toml
```

## Who this is for

- Academic optimization researchers who want a category-defining
  benchmark instance instead of yet another synthetic knapsack
- Infrastructure consultants (Bain, BCG, McKinsey infra teams) who want
  a public reference solver they can extend in client engagements
- IPP developers and sovereign AI program offices who need to ask "is
  the announced capacity feasible under joint uncertainty"
- Anyone publishing a stochastic-optimization paper who wants a
  benchmark with a real-world story attached

## What this is not

- Not a consulting product. Direct-to-hyperscaler NDA sales is not the
  business model. The business model is publish-the-benchmark.
- Not a single-axis optimizer. There are good single-axis solvers; the
  point is the joint problem.
- Not a forecasting tool. It is a decision model, not a predictor.
- Not a substitute for an Aurora / Wood Mac / ICF capacity-market
  forecast. It uses those distributions as inputs.

## License

MIT. See `LICENSE`.
