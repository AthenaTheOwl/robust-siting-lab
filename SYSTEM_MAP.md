# System map

```text
benchmarks/toy_public.json
        |
        v
robust_siting_lab.model.load_instance
        |
        +--> robust_siting_lab.model.solve_instance
        |
        +--> robust_siting_lab.scoring.compute_regret
        |
        v
results/toy_public.json
        |
        v
reports/toy_public.jsonl
```

## Modules

- `robust_siting_lab.cli` owns the no-argument validation command.
- `robust_siting_lab.model` loads the benchmark and scores candidate sites.
- `robust_siting_lab.scoring` computes announced-choice regret and its sensitivity
  to the hand-set risk weights. It also reports `optimizer_regret_vs_best`, which is
  0 by construction for the exhaustive v0.1 screen (a consistency check, not a
  measured regret); the R-RST-007 perfect-foresight regret needs scenarios and is
  not implemented.
- `scripts/validate_schemas.py` checks the benchmark schema.
- `scripts/sources_only_public.py` checks that citations are public URLs.

The v0.1 solver is an enumerator over a tiny fixture instance. Larger stochastic
decomposition remains queued.
