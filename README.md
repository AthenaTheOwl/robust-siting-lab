# Robust Siting Lab

Robust Siting Lab is a small public-source-shaped benchmark for joint grid,
water, and silicon siting risk. It asks one decision question: given a set of
candidate data-center sites and risk weights, which site has the lowest expected
cost, and how much regret does the announced choice carry?

## How to run

The first user action validates the bundled v0.1 artifact with no flags:

```powershell
python -m robust_siting_lab validate
```

To regenerate the checked result:

```powershell
python -m robust_siting_lab solve --instance benchmarks/toy_public.json --out results/toy_public.json
```

For a readable ranked result (no flags), reading the committed solution:

```powershell
python -m robust_siting_lab show
```

It prints the candidate sites ranked by expected cost, marks the optimal and
announced sites, and reports the regret the announced choice carries.

## live demo

A Streamlit app (`streamlit_app.py`) wraps the same result as an interactive page -
the ranked-site table, the optimal/announced/regret metrics, and the cost weights
with their source citations. It reads the committed `results/toy_public.json`; no
network, no secrets.

Run it locally:

```powershell
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Live: deploy on [Streamlit Community Cloud](https://share.streamlit.io) - new app,
repo `AthenaTheOwl/robust-siting-lab`, branch `main`, main file `streamlit_app.py`.

<!-- live-url: (paste the Streamlit Community Cloud URL here once deployed) -->

## What ships in v0.1

- `benchmarks/toy_public.json`: three-site toy benchmark with public-source-shaped citations.
- `benchmarks/schema.json`: benchmark shape.
- `robust_siting_lab/`: deterministic scoring and regret code.
- `results/toy_public.json`: checked solution.
- `reports/toy_public.jsonl`: one machine-readable report row.
- `PRODUCT_BRIEF.md`, `SYSTEM_MAP.md`, `STATUS.md`, and `specs/0002-design/`.

## What this is not

- Not a production siting recommendation.
- Not a live public-filing ingest.
- Not a commercial-solver benchmark.
- Not a forecast.

The next pass is to replace the toy fixture with reviewed public Meta and
Microsoft benchmark instances.

## License

MIT. See `LICENSE`.
