# Spec 0001 — Acceptance (RobustSiting)

v0 (this scaffold PR) is done when:

- `README.md`, `LICENSE`, `AGENTS.md`, `.gitignore` exist
- `specs/0001-foundation/{requirements,design,tasks,acceptance}.md` exist
- `docs/first-pr.md` describes the second PR
- README status checkboxes show the scaffold rows checked
- No code beyond what spec 0001 names lives in this repo

Spec 0002 (the next PR) is done when:

```bash
uv sync
uv run pytest                                            # all green, < 30s
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
uv run python scripts/sources_only_public.py benchmarks/
```

And:

- The solver beats a random baseline on the toy instance (regret check
  in the integration test)
- Every benchmark instance is schema-valid
- Every result file includes a regret bound against a stated baseline
- All tests run offline with no commercial solver license

Gates: `voice_lint`, `spec_check`, `validate_schemas`,
`regret_reported`, `sources_only_public`. A PR that fails any gate is
not merged.
