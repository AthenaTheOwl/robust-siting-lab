# First PR after the scaffold

This file describes the literal next PR after the v0 scaffold lands.
Spec 0002 is the work plan; this file is the file-level changeset.

## Goal

A `robust-siting solve` command that, given a benchmark instance file
and a scenario count, builds the two-stage stochastic program, runs an
L-shaped decomposition with an open-source solver, and writes a result
file containing first-stage decisions plus expected cost. A second
command `robust-siting regret` reads the result and computes regret
against the announced choice and against the perfect-foresight optimum.

The first runnable target is the toy fixture, not the public Meta or
Microsoft instances. Those land in spec 0003 alongside the paper draft.

## Files changed

New:

- `pyproject.toml` — Python 3.11, `uv`, `pyscipopt`, `highspy`,
  `numpy`, `pydantic`, `jsonschema`, `click`
- `cli/main.py` — `click` group with `solve` and `regret`
- `src/__init__.py`
- `src/model/two_stage_stochastic.py`
- `src/scenarios/grid_uncertainty.py`
- `src/scenarios/water_rights.py`
- `src/scenarios/silicon_allocation.py`
- `src/solver/decomposition.py`
- `src/eval/regret_metrics.py`
- `benchmarks/schema.json`
- `tests/fixtures/toy_instance.json`
- `tests/test_model.py`
- `tests/test_scenarios.py`
- `tests/test_solver.py`
- `tests/test_regret.py`
- `tests/test_end_to_end.py`
- `scripts/voice_lint.py`
- `scripts/spec_check.py`
- `scripts/validate_schemas.py`
- `scripts/regret_reported.py`
- `scripts/sources_only_public.py`
- `results/.gitkeep`
- `benchmarks/.gitkeep` (real instances ship in spec 0003)

Modified:

- `README.md` — replace placeholder "How to run" with the real commands
- `specs/0001-foundation/tasks.md` — check off the spec-0002 rows
- `AGENTS.md` — point Gates section at real scripts

## Verification

```bash
uv sync
uv run pytest -v                                         # < 30 s
uv run robust-siting solve \
    --instance tests/fixtures/toy_instance.json \
    --scenarios 8 \
    --out results/toy.json
uv run robust-siting regret \
    --instance tests/fixtures/toy_instance.json \
    --result results/toy.json
uv run python scripts/voice_lint.py
uv run python scripts/spec_check.py
uv run python scripts/validate_schemas.py benchmarks/
uv run python scripts/regret_reported.py results/
```

## Out of scope for this PR

- `benchmarks/meta_2026_public.json` and `benchmarks/msft_2026_public.json`
  (spec 0003)
- `paper/robust-siting.tex` (spec 0003)
- Multi-stage variants
- Solver tuning beyond defaults
