"""robust-siting-lab - live demo (Streamlit Community Cloud).

Reads the committed solution under results/toy_public.json and shows the
joint grid/water/silicon siting result: candidate sites ranked by expected
cost, the optimal pick, and the regret of the announced choice. No network,
no secrets - runs entirely off the committed benchmark artifact.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/robust-siting-lab,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent
RESULT = REPO / "results" / "toy_public.json"
INSTANCE = REPO / "benchmarks" / "toy_public.json"


def load_payload() -> tuple[dict | None, dict | None]:
    if not RESULT.is_file():
        return None, None
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    instance = json.loads(INSTANCE.read_text(encoding="utf-8")) if INSTANCE.is_file() else None
    return payload, instance


st.set_page_config(page_title="robust-siting-lab - siting risk", layout="wide")
st.title("robust-siting-lab")
st.caption(
    "joint grid/water/silicon data-center siting risk: given candidate sites and "
    "risk weights, which site has the lowest expected cost, and how much regret does "
    "the announced choice carry?"
)

payload, instance = load_payload()
if payload is None:
    st.warning("no result found under results/toy_public.json - run `python -m robust_siting_lab validate` first")
    st.stop()

solution = payload["solution"]
regret = payload["regret"]
rows = solution["scored_sites"]
selected = solution["selected_site"]
announced = solution["announced_site"]

st.subheader(f"instance: {solution['instance_id']}")

c1, c2, c3 = st.columns(3)
c1.metric("optimal site", selected, help="lowest expected cost")
c2.metric("optimal expected cost", f"{solution['selected_expected_cost']:.3f}")
c3.metric(
    "announced regret",
    f"{regret['announced_regret']:.3f}",
    help="extra expected cost the announced choice carries versus the optimal site",
)

show_only_costlier = st.checkbox(
    "show only sites costlier than the optimal", value=False
)

table = []
for i, row in enumerate(sorted(rows, key=lambda r: r["expected_cost"]), start=1):
    site = row["site_id"]
    if show_only_costlier and site == selected:
        continue
    marks = []
    if site == selected:
        marks.append("optimal")
    if site == announced:
        marks.append("announced")
    table.append(
        {
            "rank": i,
            "site": site,
            "expected cost": round(row["expected_cost"], 3),
            "note": ", ".join(marks),
        }
    )

st.dataframe(table, use_container_width=True, hide_index=True)

if announced == selected:
    st.info(f"the announced choice {announced} is the optimal site - zero regret.")
else:
    pct = 100 * regret["announced_regret"] / solution["selected_expected_cost"]
    st.info(
        f"announced choice **{announced}** costs {solution['announced_expected_cost']:.3f}, "
        f"carrying regret of **{regret['announced_regret']:.3f}** ({pct:.1f}% over optimal) "
        f"versus picking **{selected}**."
    )

if instance is not None:
    with st.expander("cost weights and source citations"):
        weights = instance.get("cost_weights", {})
        cites = instance.get("citations", {})
        st.write(
            [
                {"factor": k, "weight": v, "source": cites.get(k, "")}
                for k, v in weights.items()
            ]
        )
