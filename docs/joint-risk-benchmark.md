# A weighted screen is the baseline for a joint-risk experiment

Method update: October 18, 2026. Proposed experiments below are not reported as executed results.

The shipped `site_expected_cost` function adds weighted capex and weighted grid, water and silicon risk proxies. `solve_instance` ranks those deterministic totals. This is an inspectable screening baseline; it does not currently solve a two-stage stochastic program, represent joint scenarios, or model recourse. Regret against the best score in the same instance measures disagreement with that screen.

The next proposed benchmark should make joint uncertainty explicit. Use a synthetic common shock that simultaneously delays grid equipment and silicon, plus an independent water scenario. Freeze probabilities, site decisions, recourse options and cost units before comparing policies. Include the deterministic screen, a scenario-aware fixed decision and a recourse policy on the same held-out draws.

Report expected cost, tail cost, unmet demand and infeasibility separately. A low mean cannot compensate for a failed hard feasibility condition. Name the baseline used for each regret value; a within-model zero is not a bound on real-world regret. Keep this method note beside the current baseline until the scenario-aware implementation and its acceptance tests exist.

## References

- Birge, J. R. and Louveaux, F. (2011). *Introduction to Stochastic Programming*, 2nd ed. Springer. https://doi.org/10.1007/978-1-4614-0237-4. Two-stage stochastic programs with recourse, the formulation the proposed benchmark would test against the screen.
- Boyd, S. and Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/. General background on the optimization formulations; not a source for any specific claim above.
