# Spec 0002 acceptance

The v0.1 release is accepted when:

- `python -m robust_siting_lab validate` exits 0 with no flags.
- `python -m pytest -q` passes.
- `reports/toy_public.jsonl` exists and contains announced regret.
- citation values use public URL prefixes.
