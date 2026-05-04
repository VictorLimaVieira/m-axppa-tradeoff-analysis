# Case Study V1 - Approximate Computing Trade-off Analysis

## Context

Approximate computing is a strategy used to reduce energy consumption,
hardware area, and computational cost by accepting small controlled errors.
This approach is especially relevant in error-tolerant applications such as
image processing, video processing, signal processing, and some artificial
intelligence workloads.

This project was inspired by a public paper about **M-AxPPA: Modified
Approximate Parallel Prefix Adder**, presented in an academic context. The
portfolio goal is not to claim authorship of the original architecture, but to
translate the technical problem into a data analysis case study.

## Data Problem

The central question is:

> Given a set of approximate architectures, which configurations provide the
> best balance between error, energy savings, and area savings?

This is a classic multi-objective decision problem. One architecture may save a
large amount of energy while producing high error. Another may preserve
accuracy while saving less area.

## Data

Because the complete experimental data is not available for public disclosure,
V1 uses synthetic data based on the public structure described in the paper.

The dataset contains:

- 315 M-AxPPA architectures;
- 128 literature baseline architectures;
- 443 architectures in total;
- error and quality metrics, such as `SSIM`, `NCC`, `MAE`, `MRE`, and `MRED`;
- synthesis metrics, such as energy savings and area savings.

The synthetic data is used to demonstrate the analytical workflow, not to claim
real hardware measurements.

## Method

The project was organized into six stages:

1. Generate and organize the data.
2. Model the data in a SQLite database.
3. Write SQL queries to answer ranking and filtering questions.
4. Prepare a curated dataset for Power BI.
5. Build a Power BI dashboard to compare error, energy, and area.
6. Publish an interactive Streamlit dashboard for online exploration.

The main analytical logic is:

```text
First, filter architectures by acceptable error.
Then, rank the remaining candidates by energy, area, or balanced score.
```

Pareto candidates were also flagged to highlight architectures that are not
dominated in the error-energy and error-area trade-offs.

## V1 Deliverables

The first public version of the project includes:

- synthetic dataset structured for analysis;
- SQLite database with a relational schema;
- SQL queries for rankings, error filters, and Pareto candidates;
- Excel/CSV dataset prepared for Power BI;
- Power BI dashboard comparing energy, area, error, and variants;
- dashboard screenshot in the README;
- deployed Streamlit dashboard;
- analytical questions documentation to frame the project as a BI case.

## Initial Results

In the synthetic dataset, when architectures are filtered by `MRED <= 0.10`,
some candidates show high energy savings with controlled error.

Example of a strong energy-saving candidate:

```text
M-AxPPA-LOA, M=1, L=1, K=14
MRED: 0.0828
Energy savings: 91.44%
Area savings: 59.26%
```

Example of a balanced candidate:

```text
M-AxPPA-LOA, M=2, L=1, K=13
MRED: 0.0710
Energy savings: 88.62%
Area savings: 60.93%
```

When the objective changes from energy to area, the ranking changes. This shows
that the best architecture depends on the business or engineering question.

The Pareto analysis reinforces this point: some architectures are relevant
because they deliver higher savings with controlled error, while others become
more attractive when the priority is area reduction. The final decision depends
on the criterion selected for the application.

## Data Skills Demonstrated

This project demonstrates:

- experimental data modeling;
- SQL queries with `JOIN`, `WHERE`, `ORDER BY`, and filters;
- trade-off analysis between conflicting metrics;
- multi-objective analysis with Pareto candidates;
- dataset preparation for BI;
- Power BI dashboard design;
- Streamlit dashboard deployment;
- technical storytelling for decision-making.

## Limitations

The V1 results use synthetic data. They are useful for demonstrating the
analysis workflow, but they should not be interpreted as real hardware
measurements.

A future version may replace or complement this dataset with real experimental
data if public disclosure becomes possible.

## Next Steps

- Extend the exploratory data analysis notebook with more statistical views.
- Improve documentation for the deployed Streamlit version.
- Evolve the Power BI dashboard with a second ranking page.
