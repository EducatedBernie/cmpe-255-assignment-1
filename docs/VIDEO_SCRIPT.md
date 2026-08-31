# YouTube Walkthrough Script

Target length: 6–8 minutes. Record your own narration so you can demonstrate that you understand the work.

## 0:00–0:35 — Assignment and repository

**Show:** GitHub repository README and folder tree.

**Say:**

“This is my CMPE 255 Assignment 1 submission. I used Codex as an agentic coding assistant to build and verify an end-to-end Adult Income data-science project. The repository includes the source code, tests, generated metrics and figures, a prompt record, a Medium article draft, and this walkthrough.”

## 0:35–1:15 — Dataset and objective

**Show:** `data/README.md` and `artifacts/figures/income_distribution.png`.

**Say:**

“The Adult dataset has 48,842 records and 14 predictors. The task is binary classification: estimate whether annual income exceeds $50,000. About 24% of the records are in the positive class, so the data is imbalanced and accuracy cannot be interpreted by itself.”

## 1:15–2:10 — End-to-end pipeline

**Show:** `src/analysis.py`, briefly highlighting `clean_adult`, the train/test split, `ColumnTransformer`, and model dictionary.

**Say:**

“The pipeline validates the schema, removes whitespace, normalizes the target labels, and leaves missing predictors for imputation. I split before fitting preprocessing. Numeric columns use median imputation and standardization; categorical columns use most-frequent imputation and one-hot encoding. Keeping this inside each model pipeline prevents leakage from the test set.”

## 2:10–2:45 — Tests and reproducibility

**Show:** run `.venv/bin/python -m unittest discover -s tests -v`.

**Say:**

“The tests cover data-file loading, malformed schemas, cleaning, deterministic results, and required output files. The fixed random seed is 42. The whole experiment runs with one command: `python -m src.analysis`.”

## 2:45–4:00 — Classification results

**Show:** `artifacts/figures/model_comparison.png` and `artifacts/metrics.csv`.

**Say:**

“The dummy baseline reaches 76.07% accuracy by always predicting the majority class, but its recall and F1 for the high-income class are zero. Random forest reaches 83.82% accuracy, 80.28% recall, 0.7037 F1, and 0.917 ROC-AUC. Logistic regression has slightly better recall at 83.70%, but lower precision and F1. I selected random forest as the best balanced benchmark, not as a universally best model.”

## 4:00–4:45 — Interpreting features

**Show:** `artifacts/figures/feature_importance.png`.

**Say:**

“Age, marital and relationship categories, education level, capital gain, and hours worked have high impurity-based importance in the forest. These are associations learned from historical data. They are not causal explanations, and correlated features can split importance between them.”

## 4:45–5:35 — Part 2 replications

**Show:** `artifacts/summary.json` and `docs/RESULTS.md`.

**Say:**

“For Part 2, I adapted the instructor repository's clustering, anomaly detection, and audit themes. Four-cluster K-means gave a low 0.2013 silhouette score, so I do not claim strong natural segments. Isolation Forest flagged 5% because I explicitly set its contamination threshold to 5%; that is a ranking cutoff, not a discovered population fact.”

## 5:35–6:30 — Audit and limitations

**Show:** `artifacts/group_metrics.csv` and the responsible-use section of the README.

**Say:**

“The random forest's recall is 65.67% for records marked female and 83.00% for records marked male. A slice like this does not complete a fairness evaluation, but it exposes behavior hidden by aggregate accuracy. Because the data reflects 1994 patterns and contains sensitive attributes, I recommend educational use only—not consequential decisions.”

## 6:30–7:10 — Agentic journey and conclusion

**Show:** `docs/PROMPTS_AND_PROCESS.md`, then return to README.

**Say:**

“Codex helped read the assignment, implement tests and code, execute the experiments, and draft artifacts. My responsibility was to review the evidence and explain what it does and does not support. The main lesson is that agentic coding can accelerate the journey, but reliable data science still depends on baselines, leakage control, honest negative findings, and responsible interpretation.”

## Recording checklist

- Use 1080p screen capture and enlarge terminal/editor text.
- Run the tests live; do not expose personal notifications or credentials.
- Show the public repository URL in the browser after publication.
- Upload the video as **Unlisted** or **Public**, according to instructor requirements.
- Replace the pending YouTube entry in `README.md` with the final URL.
