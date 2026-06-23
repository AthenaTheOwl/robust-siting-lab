"""robust-siting-lab - live demo (Streamlit Community Cloud).

Reads the committed solution under results/toy_public.json and shows the
joint grid/water/silicon siting result: candidate sites ranked by expected
cost, the optimal pick, and the regret of the announced choice. Then lets the
user edit the candidate sites' risks/capex and the cost weights and re-runs the
REAL solver (robust_siting_lab.model.solve_instance + scoring.compute_regret)
live - no network, no secrets, the actual engine the CLI uses.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/robust-siting-lab,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import streamlit as st

from robust_siting_lab.model import solve_instance
from robust_siting_lab.scoring import compute_regret

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

# ---------------------------------------------------------------------------
# interactive: site your own scenario -> drive the REAL solver live
# ---------------------------------------------------------------------------
st.divider()
st.header("site it yourself")
st.caption(
    "edit the candidate sites and the risk weights below, then re-solve. this "
    "calls the same engine the CLI uses - `robust_siting_lab.model.solve_instance` "
    "and `robust_siting_lab.scoring.compute_regret` - on your input. nothing is "
    "hardcoded: change a risk or a weight and watch the optimal pick and the "
    "announced regret move."
)

# seed the editable scenario from the committed instance (or a fallback).
seed = copy.deepcopy(instance) if instance is not None else {
    "instance_id": "custom",
    "candidate_sites": [
        {"site_id": "site-a", "capex_billion": 8.0, "grid_delay_risk": 0.3,
         "water_shortfall_risk": 0.2, "silicon_delay_risk": 0.2},
    ],
    "cost_weights": {"capex": 1.0, "grid_delay": 2.4, "water_shortfall": 1.8,
                     "silicon_delay": 1.3},
    "announced_choice": {"site_id": "site-a"},
}
sites = seed["candidate_sites"]
seed_weights = seed["cost_weights"]
site_ids = [s["site_id"] for s in sites]

st.subheader("risk weights")
st.caption("how much each factor counts toward expected cost (higher = matters more)")
wc = st.columns(4)
w_capex = wc[0].slider("capex", 0.0, 5.0, float(seed_weights["capex"]), 0.1)
w_grid = wc[1].slider("grid delay", 0.0, 5.0, float(seed_weights["grid_delay"]), 0.1)
w_water = wc[2].slider("water shortfall", 0.0, 5.0, float(seed_weights["water_shortfall"]), 0.1)
w_silicon = wc[3].slider("silicon delay", 0.0, 5.0, float(seed_weights["silicon_delay"]), 0.1)

st.subheader("candidate sites")
st.caption("edit each site's capex (billions) and its three risk probabilities (0-1)")
edited_sites = []
for s in sites:
    st.markdown(f"**{s['site_id']}**")
    cc = st.columns(4)
    capex = cc[0].number_input(
        "capex $B", min_value=0.0, max_value=50.0,
        value=float(s["capex_billion"]), step=0.1, key=f"capex_{s['site_id']}",
    )
    grid = cc[1].slider(
        "grid delay risk", 0.0, 1.0, float(s["grid_delay_risk"]), 0.01,
        key=f"grid_{s['site_id']}",
    )
    water = cc[2].slider(
        "water shortfall risk", 0.0, 1.0, float(s["water_shortfall_risk"]), 0.01,
        key=f"water_{s['site_id']}",
    )
    silicon = cc[3].slider(
        "silicon delay risk", 0.0, 1.0, float(s["silicon_delay_risk"]), 0.01,
        key=f"silicon_{s['site_id']}",
    )
    edited_sites.append({
        "site_id": s["site_id"],
        "capex_billion": capex,
        "grid_delay_risk": grid,
        "water_shortfall_risk": water,
        "silicon_delay_risk": silicon,
    })

default_idx = (
    site_ids.index(seed.get("announced_choice", {}).get("site_id", site_ids[0]))
    if site_ids else 0
)
announced_pick = st.selectbox(
    "announced choice (the site already publicly committed to)",
    site_ids, index=default_idx,
)

# build a fresh instance and call the REAL engine.
live_instance = {
    "instance_id": "live",
    "candidate_sites": edited_sites,
    "cost_weights": {
        "capex": w_capex,
        "grid_delay": w_grid,
        "water_shortfall": w_water,
        "silicon_delay": w_silicon,
    },
    "announced_choice": {"site_id": announced_pick},
}

live_solution = solve_instance(live_instance)
live_regret = compute_regret(live_solution)

st.subheader("re-solved result")
m1, m2, m3 = st.columns(3)
m1.metric("optimal site", live_solution["selected_site"], help="lowest expected cost")
m2.metric("optimal expected cost", f"{live_solution['selected_expected_cost']:.3f}")
m3.metric(
    "announced regret",
    f"{live_regret['announced_regret']:.3f}",
    help="extra expected cost the announced choice carries vs the optimal site",
)

live_table = [
    {
        "rank": i,
        "site": row["site_id"],
        "expected cost": round(row["expected_cost"], 3),
        "note": ", ".join(
            m for m in (
                "optimal" if row["site_id"] == live_solution["selected_site"] else "",
                "announced" if row["site_id"] == live_solution["announced_site"] else "",
            ) if m
        ),
    }
    for i, row in enumerate(live_solution["scored_sites"], start=1)
]
st.dataframe(live_table, use_container_width=True, hide_index=True)

if live_solution["announced_site"] == live_solution["selected_site"]:
    st.success(
        f"under these weights the announced choice **{live_solution['announced_site']}** "
        f"IS the optimal site - zero regret."
    )
else:
    live_pct = (
        100 * live_regret["announced_regret"] / live_solution["selected_expected_cost"]
        if live_solution["selected_expected_cost"] else 0.0
    )
    st.warning(
        f"announced choice **{live_solution['announced_site']}** costs "
        f"{live_solution['announced_expected_cost']:.3f}, carrying regret of "
        f"**{live_regret['announced_regret']:.3f}** ({live_pct:.1f}% over optimal) "
        f"versus picking **{live_solution['selected_site']}**."
    )
