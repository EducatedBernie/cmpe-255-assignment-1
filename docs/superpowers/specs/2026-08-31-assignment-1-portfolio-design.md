# CMPE 255 Assignment 1 Portfolio Design

## Goal

Create a public-repository-ready Assignment 1 submission that demonstrates an agent-assisted, end-to-end data-science workflow and a focused replication of representative experiments from the instructor's reference repository.

## Scope

Use the Adult/Census Income dataset because it is the dataset in the instructor's worked ChatGPT transcript and is also published on Kaggle. One reproducible Python pipeline will cover:

- CRISP-DM framing and data understanding
- cleaning and preprocessing
- exploratory visualizations
- baseline and comparative classification models
- customer-style demographic clustering
- anomaly detection
- leakage/reproducibility audit notes

This intentionally adapts three prompt-catalog themes—classification, clustering, and anomaly detection—rather than copying all 14 reference applications. The submission will state that scope plainly.

## Architecture

`src/analysis.py` owns the deterministic analysis pipeline. It downloads the public UCI source files when absent, validates their schema, trains only scikit-learn pipelines, and writes all derived artifacts under `artifacts/`. `tests/test_analysis.py` checks cleaning, schema validation, and reproducible model output on a small in-memory fixture.

Human-facing deliverables live in the repository root and `docs/`: a primary README, prompt/process log, report, and Medium draft. The README links the published YouTube walkthrough. Generated metrics and images are committed so the repository remains reviewable without rerunning training.

## Data and Ethics

The source is the UCI Adult dataset (48,842 records, 14 predictors), mirrored on Kaggle as Adult Census Income. The target is whether annual income exceeds $50K. Because the data contains sensitive demographic attributes and reflects 1994 US Census-era patterns, the report will frame results as a teaching demonstration—not a suitable automated decision system—and will report group-level performance slices without claiming fairness.

## Verification

- Unit tests must pass with Python's built-in `unittest`.
- The full pipeline must exit successfully and regenerate every documented artifact.
- Generated metrics must include a dummy baseline and at least two learned classifiers.
- The README must link every local artifact and the published YouTube walkthrough.
