# Spec 0002 design

The first runnable pass narrows the foundation design to a tiny offline
benchmark. The model enumerates candidate sites and scores each with capex,
grid-delay, water-shortfall, and silicon-delay weights. This keeps the v0.1
solver understandable while preserving the larger stochastic-program shape.
