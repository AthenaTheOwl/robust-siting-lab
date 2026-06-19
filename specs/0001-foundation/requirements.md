# Spec 0001 — Foundation (RobustSiting)

## R-RST-001 — repo scaffold
Repo lives at `e:/claude_code/random-apps/robust-siting-lab`. MIT
license, copyright Vignesh Gopalakrishnan. README, AGENTS.md,
.gitignore, and `specs/0001-foundation/` exist before any runnable
code lands.

## R-RST-002 — benchmark instance schema
`benchmarks/schema.json` defines the JSON shape of a benchmark
instance: candidate sites, capacity tiers, grid scenarios, water
scenarios, silicon scenarios, announced choice (the ground-truth
baseline), and a citations block mapping every input value to a public
source URL.

## R-RST-003 — public-sources discipline
Every benchmark instance must cite a public source for every numeric
input. A script `scripts/sources_only_public.py` walks the citations
block and asserts URLs resolve to a public filing or report. No
hyperscaler-internal data.

## R-RST-004 — two-stage stochastic model
`src/model/two_stage_stochastic.py` encodes the model: first-stage
siting decisions (where, how many MW), second-stage operational
decisions per scenario. Cost function combines capex, expected lost
load, water-shortfall penalty, and silicon-delay penalty.

## R-RST-005 — scenario modules
Three modules emit scenario draws: `src/scenarios/grid_uncertainty.py`
(interconnection-queue survival distributions), `water_rights.py`
(drought + basin-allocation scenarios), `silicon_allocation.py` (CoWoS
+ HBM + substrate bottleneck scenarios). Each module reads its
parameters from the benchmark instance and emits N seeded scenarios.

## R-RST-006 — decomposition solver
`src/solver/decomposition.py` implements an L-shaped or Benders-style
decomposition over the scenario set. The solver is callable from the
CLI and returns first-stage decisions plus expected cost.

## R-RST-007 — regret evaluation
`src/eval/regret_metrics.py` computes the regret of the
announced-choice solution against the optimizer's recommendation, and
the regret of the optimizer's recommendation against the perfect-
foresight per-scenario optimum. Both bounds are required outputs.

## R-RST-008 — first benchmark instance
`benchmarks/meta_2026_public.json` is the first published instance,
modeled on Meta's publicly disclosed 2026 expansion filings, with full
citations. `benchmarks/msft_2026_public.json` is the second.

## R-RST-009 — paper draft
`paper/robust-siting.tex` is the arxiv paper draft, with sections:
problem statement, model, decomposition, benchmark, results,
discussion. The paper compiles in CI on every PR.

## R-RST-010 — gates
Five gates run in CI and locally: `voice_lint.py`, `spec_check.py`,
`validate_schemas.py`, `regret_reported.py`, `sources_only_public.py`.
A PR that fails any gate does not merge.

## R-RST-011 — fixture instance
`tests/fixtures/toy_instance.json` is a small synthetic instance (3
sites, 2 capacity tiers, 8 scenarios) so the test suite runs in under
30 seconds with no commercial solver dependency.
