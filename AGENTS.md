# AGENTS.md — robust-siting-lab

Operating contract for AI agents (Claude, Codex, Cursor) working in this
repo. Conventions match the rest of the AthenaTheOwl portfolio so an
agent already trained on semiconductor-wafer-robust-optimization,
facility-location, or world-food-program-robust-simulator recognizes
the shape.

## What this repo is

An open benchmark and reference solver for two-stage stochastic
optimization of AI data-center siting under joint uncertainty in grid,
water, and silicon. The benchmark instance schema, the solver, and the
regret-bound evaluation script are the deliverables. The paper is a
companion artifact.

## Roles you may see in tasks

| Role | What they do |
|---|---|
| `scenario-author` | Draws scenarios from the three uncertainty modules |
| `instance-curator` | Maintains `benchmarks/*.json` from public filings only |
| `model-builder` | Encodes the two-stage stochastic program |
| `solver-runner` | Runs decomposition; emits first-stage decisions plus expected cost |
| `regret-evaluator` | Computes regret bounds against announced choices |
| `paper-author` | Maintains `paper/robust-siting.tex` |

These roles exist in the spec ledger; v0 does not implement them.

## Voice constraints

- No marketing words.
- No antithetical reversals as a structural device.
- Plain assertions. The math and the public-data benchmark are the
  moat; the writing is scaffolding.

## Gates (will land in spec 0002)

- `voice_lint.py` mirrored from athena-site
- `spec_check.py` — every `R-RST-*` ID is implemented or tested by the
  time its parent PR merges
- `validate_schemas.py` — every `benchmarks/*.json` validates against
  `benchmarks/schema.json`
- `regret_reported.py` — every solver run that publishes a result must
  include a regret bound against a stated baseline
- `sources_only_public.py` — every benchmark instance must cite a
  publicly accessible filing or report for each input fact

## Out of scope

- Hyperscaler-internal data. The benchmark uses only public filings,
  permit applications, and disclosed expansion plans.
- A live capacity-market forecast. Aurora / Wood Mac / ICF already do
  this; the model consumes their distributions as inputs, doesn't
  replace them.
- A SaaS solver. The repo is a CLI plus a paper plus benchmark files.
- Single-axis optimization. The point is joint grid+water+silicon
  uncertainty.
