# Analytical Questions

This page translates the engineering problem into decision-oriented analytical
questions. The goal is to make the project easier to read as a data and BI
portfolio case, not only as a technical approximate-computing experiment.

## Business And Engineering Questions

1. Which architectures maximize energy savings under `MRED <= 0.10`?
2. Which architectures maximize area savings under `MRED <= 0.10`?
3. Which variants dominate the Pareto frontier?
4. How does the best architecture change when the decision criterion changes?
5. Which configurations offer the best balanced trade-off?

## Decision Logic

The recommended workflow is:

```text
1. Define an acceptable error threshold.
2. Filter candidate architectures by MRED.
3. Compare energy savings, area savings, and balanced score.
4. Use Pareto candidates to identify architectures that are not dominated.
5. Choose a candidate according to the application priority.
```

## Interpretation

An architecture with high energy savings is not automatically the best option.
For error-tolerant systems, the decision depends on the acceptable quality loss
and on whether the application prioritizes energy, silicon area, or a balanced
trade-off between both.
