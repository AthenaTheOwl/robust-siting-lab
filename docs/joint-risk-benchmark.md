# A weighted screen is the baseline for a joint-risk experiment

Method update: October 18, 2026. Proposed experiments below are not reported as executed results.

The shipped `site_expected_cost` function adds weighted capex and weighted grid, water and silicon risk proxies. `solve_instance` ranks those deterministic totals. This is an inspectable screening baseline; it does not currently solve a two-stage stochastic program, represent joint scenarios, or model recourse. Regret against the best score in the same instance measures disagreement with that screen.

The next proposed benchmark should make joint uncertainty explicit. Use a synthetic common shock that simultaneously delays grid equipment and silicon, plus an independent water scenario. Freeze probabilities, site decisions, recourse options and cost units before comparing policies. Include the deterministic screen, a scenario-aware fixed decision and a recourse policy on the same held-out draws.

Report expected cost, tail cost, unmet demand and infeasibility separately. A low mean cannot compensate for a failed hard feasibility condition. Name the baseline used for each regret value; a within-model zero is not a bound on real-world regret. Keep this method note beside the current baseline until the scenario-aware implementation and its acceptance tests exist.

## References

- https://doi.org/10.1287/opre.1030.0065
- https://web.stanford.edu/~boyd/cvxbook/
