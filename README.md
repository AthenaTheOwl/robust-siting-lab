# robust-siting-lab

A data center gets announced on a campus in Arizona. The lab scores three candidate
sites and finds that one carries 2.2% more expected cost than the cheapest option
once you price in grid delay, water shortfall, and silicon delay. That 2.2% is the
regret on the announced choice — the part the press release doesn't mention.

## What it does

A siting decision pretends to be about land and dollars. It's really about three
clocks that don't agree: the interconnection queue, the water table, and the chip
order. A campus with the lowest capex can still be the wrong site if the grid won't
energize it, the river won't supply it, or the silicon won't arrive. Those risks sit
in separate filings — FERC, the Bureau of Reclamation, BIS, the SEC — and nobody adds
them into one number.

robust-siting-lab adds them into one number. It takes a set of candidate sites, each
with a capex and three risk fields, weights them, and ranks the sites by expected
cost. Then it looks at the site that was actually announced and reports the regret:
how much the announced choice costs over the optimum. v0.1 ships one toy benchmark as
a checked-in instance, scored deterministically. The model and the regret math are
the point; the data adapter is deliberately small. Every numeric field carries a
public-source-shaped citation URL, and the gate runs with no network access.

## Try it

No flags, no setup, no keys. It reads the committed solution and prints the ranking:

```powershell
python -m robust_siting_lab show
```

```
robust-siting-lab - joint grid/water/silicon siting risk, instance=toy_public
3 candidate site(s), ranked by expected cost (lower is better)

rank  site            expected cost   note
------------------------------------------
   1  ercot-west              9.474   optimal
   2  pjm-west                9.596   
   3  az-campus               9.686   announced

lowest expected cost: ercot-west at 9.474.
announced choice az-campus costs 9.686, carrying regret of 0.212 (2.2% over optimal) versus picking ercot-west.
```

The optimal site is at the top, the announced site is wherever the weighted risk puts
it, and the gap between them is the regret.

## Live demo

A Streamlit app (`streamlit_app.py`) wraps the same result as an interactive page —
the ranked-site table, the optimal/announced/regret metrics, and the cost weights with
their source citations. It reads the committed `results/toy_public.json`; no network,
no secrets.

Run it locally:

```powershell
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Live: deploy on [Streamlit Community Cloud](https://share.streamlit.io) - new app,
repo `AthenaTheOwl/robust-siting-lab`, branch `main`, main file `streamlit_app.py`.

<!-- live-url: (paste the Streamlit Community Cloud URL here once deployed) -->

## How it connects

robust-siting-lab is the decision layer over the same buildout the energy repos track.
The risk fields it weights come from the projects that score them upstream:

- [grid-silicon](https://github.com/AthenaTheOwl/grid-silicon) — scores how much of an
  announced megawatt is real, which is the grid-delay risk before it's a weight here.
- [site-atlas](https://github.com/AthenaTheOwl/site-atlas) — the civic-data front end
  over the same queue these candidate sites are drawn from.

## Run it in full

The no-argument gate validates the bundled v0.1 artifact:

```powershell
python -m robust_siting_lab validate
```

Regenerate the checked result:

```powershell
python -m robust_siting_lab solve --instance benchmarks/toy_public.json --out results/toy_public.json
```

## Layout

```
robust_siting_lab/         cli, model (load + solve), scoring (regret)
benchmarks/toy_public.json the three-site fixture + public-source citations
benchmarks/schema.json     the benchmark shape
results/toy_public.json    the checked solution
reports/toy_public.jsonl   one machine-readable report row
scripts/  specs/  tests/   schema + sources-public checks, design, gate
```

The next pass replaces the toy fixture with reviewed public benchmark instances.

## License

MIT. See [LICENSE](LICENSE).
