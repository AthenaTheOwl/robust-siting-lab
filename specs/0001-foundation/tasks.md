# Spec 0001 — Tasks (RobustSiting)

First PR (the scaffold — this commit):

- [x] R-RST-001 scaffold: README + LICENSE + AGENTS.md + .gitignore
- [x] R-RST-001 specs/0001-foundation/{requirements,design,tasks,acceptance}.md
- [x] R-RST-001 docs/first-pr.md

Second PR (foundation runnable code):

- [ ] R-RST-002 `benchmarks/schema.json`
- [ ] R-RST-011 `tests/fixtures/toy_instance.json` synthetic 3-site instance
- [ ] R-RST-004 `src/model/two_stage_stochastic.py` builder
- [ ] R-RST-005 `src/scenarios/grid_uncertainty.py` survival draws
- [ ] R-RST-005 `src/scenarios/water_rights.py` drought draws
- [ ] R-RST-005 `src/scenarios/silicon_allocation.py` bottleneck draws
- [ ] R-RST-006 `src/solver/decomposition.py` L-shaped solver on toy
- [ ] R-RST-007 `src/eval/regret_metrics.py` perfect-foresight regret
- [ ] CLI: `cli/main.py` with `solve`, `regret` subcommands
- [ ] R-RST-010 `scripts/voice_lint.py`, `scripts/spec_check.py`,
      `scripts/validate_schemas.py`, `scripts/regret_reported.py`,
      `scripts/sources_only_public.py`
- [ ] Tests: one per requirement, all offline

Third PR (first real benchmark + paper draft):

- [ ] R-RST-008 `benchmarks/meta_2026_public.json` with citations
- [ ] R-RST-008 `benchmarks/msft_2026_public.json` with citations
- [ ] R-RST-009 `paper/robust-siting.tex` first draft compiling in CI
- [ ] `results/meta_2026_public.json` + `results/msft_2026_public.json`
      committed alongside the paper
