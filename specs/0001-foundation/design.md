# Spec 0001 — Design (RobustSiting)

## Model shape

Two-stage stochastic program:

```
minimize   c_x · x + E_ω [ Q(x, ω) ]
subject to A x ≤ b           (first-stage feasibility: siting, capacity)
           x ∈ X             (integer; site selected, tier picked)

Q(x, ω) = min  c_y · y(ω)
          s.t. T(ω) x + W y(ω) ≤ h(ω)
               y(ω) ≥ 0
```

- First stage: which sites to commit to, at what nameplate, with what
  build sequence
- Second stage (per scenario ω): operational dispatch given realized
  grid energization timing, water availability, and silicon delivery
- ω draws from the joint product of `grid_uncertainty`,
  `water_rights`, `silicon_allocation`

## Module map

```
src/
  model/
    two_stage_stochastic.py    # builds the program from a benchmark instance
  scenarios/
    grid_uncertainty.py        # Kaplan-Meier / survival-curve draws
    water_rights.py            # basin allocation + drought scenarios
    silicon_allocation.py      # CoWoS / HBM / substrate bottleneck scenarios
  solver/
    decomposition.py           # L-shaped / Benders
  eval/
    regret_metrics.py
benchmarks/
  schema.json
  meta_2026_public.json
  msft_2026_public.json
cli/
  main.py
paper/
  robust-siting.tex
```

## Benchmark instance shape

```json
{
  "instance_id": "meta_2026_public",
  "candidate_sites": [
    {"id": "site-1", "iso": "ERCOT", "max_mw": 1500, "citations": ["..."]},
    ...
  ],
  "scenarios": {
    "grid": {"distribution": "kaplan_meier", "params": {...}, "citations": ["..."]},
    "water": {"distribution": "drought_basin", "params": {...}, "citations": ["..."]},
    "silicon": {"distribution": "bottleneck", "params": {...}, "citations": ["..."]}
  },
  "cost_function": {
    "capex_per_mw": 8.5e6,
    "lost_load_penalty_per_mwh": 9000,
    ...
  },
  "announced_choice": {
    "sites": [{"id": "site-1", "mw": 1200}, ...],
    "citation": "..."
  }
}
```

## Solver choice

v0 uses the open-source SCIP solver via PySCIPOpt, with a fallback to
HiGHS for the LP subproblems. The fixture instance is small enough that
the test suite runs without a commercial solver license.

## Reproducibility

- Scenario sampling uses a seed pinned in the benchmark instance
- The arxiv paper builds in CI on every PR
- Every reported result in the paper links to a `results/*.json` file
  committed in the same PR

## Test discipline

- One unit test per `R-RST-*` requirement
- One integration test that solves the toy fixture and asserts the
  optimizer beats the random baseline on regret
- All tests run offline, no commercial solver, under 30 seconds
