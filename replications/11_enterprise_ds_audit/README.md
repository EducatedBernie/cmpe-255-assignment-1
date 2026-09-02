# Replication 5: Enterprise Data-Science Audit

**Reference:** Project 11, Enterprise DS Audit.

The audit checks deterministic seeds, train-only preprocessing, baseline comparison, test coverage, historical-data limitations, and group-level diagnostics.

## Result

Random-forest recall for the `>50K` class was **0.6567** for records marked female and **0.8300** for records marked male. This is not a complete fairness verdict, but it is a material gap and supports the recommendation against consequential deployment.

## Evidence

- [Group metrics](../../artifacts/group_metrics.csv)
- [Plain-language audit conclusion](../../docs/RESULTS.md)
- [Tests](../../tests/)
