# Part 2 supplemental walkthrough: recording script

Prepared September 6, 2026. Covers the existing local additions: reference 04 association mining, 07 AutoML-style search, and 12 forecasting. **Recording and upload are still pending.**

Scope confirmed by the author on September 6, 2026: any six reference projects may be selected, with the simplest acceptable adaptations preferred. The selected six remain 03, 04, 06, 07, 11, and 12. This script describes their implemented scope; recording and upload remain pending.

## Preparation

Open the root README, `replications/README.md`, `src/replications.py`, and each addition's artifacts. Use a readable editor font and enlarge plots. Hide unrelated browser tabs and any credentials. Rehearse until you can explain the concepts without simply reading the script.

From the repository root, run these before recording:

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m src.analysis
.venv/bin/python -m src.replications
```

The September 6 verification passed all eight tests and reproduced nine association rules, AutoML-style best CV ROC-AUC 0.9169, and Ridge MAPE 0.0315. Check the fresh output before quoting these values. Model fitting can be pre-run; explain that the displayed artifacts come from that run.

## 0:00–0:45 — Explain what this adds

**Show:** `replications/README.md`, with all six mappings visible.

“This is the supplement to my original Adult Income walkthrough. The original project included clustering, anomaly detection, and an enterprise-style audit. I added three distinct experiments: categorical association rules, automated model comparison, and time-series forecasting.

“These are creative adaptations of the instructor's project ideas. They are reproducible experiments with code and saved results. I am not claiming that I rebuilt every frontend or every feature of the reference applications. I will explain the input, method, result, and limitation of each addition.”

## 0:45–3:30 — Association rules

**Show:** `replications/04_associative_pattern_mining/README.md`, then `mine_association_rules` and `artifacts/rules.csv` in that directory.

“The first addition asks which categorical values frequently occur together. Instead of shopping baskets, each Adult Income record is a small basket containing education, occupation, marital status, and income category. Prefixing each value with its column name keeps categories unambiguous.

“The code counts individual items and all unordered pairs in each basket. It then evaluates both directions of every pair. Because each record has at most four selected items, there are at most six pairs per record. Direct counting is sufficient here. This is not a general implementation of Apriori or FP-Growth, and it does not search for rules with multi-item antecedents.

“Support is the fraction of all records containing both items. Confidence for A implying B is the fraction of A records that also contain B. Lift divides that confidence by B's overall frequency. Lift above one means B appears more often among A records than in the full dataset; it does not establish causation.”

**Show:** `artifacts/top_rules.png`; point to the strongest rule and its CSV row.

“With minimum support eight percent and confidence sixty percent, the run finds nine rules. The highest-lift rule goes from income above fifty thousand to married-civilian-spouse status: support 20.44 percent, confidence 85.43 percent, and lift about 1.8645.

“The direction matters. This result says about 85 percent of high-income records have that marital-status value. It does not say 85 percent of married people have high income. These are descriptive associations in an old dataset, not personal advice or evidence that one attribute causes another.”

**Understanding check:** Explain the difference between a common consequent producing high confidence and a rule producing high lift. Be able to calculate confidence from pair count divided by antecedent count.

## 3:30–6:15 — AutoML-style candidate comparison

**Show:** `benchmark_models`, especially preprocessing, candidate definitions, and `StratifiedKFold`.

“The second addition automates comparison across four fixed model candidates: logistic regression, random forest, extra trees, and histogram gradient boosting. It uses a deterministic sample of twelve thousand Adult records and three stratified folds. Stratification preserves the class balance approximately in each fold.

“For every candidate and fold, numeric missing values are imputed and scaled, and categorical values are imputed and one-hot encoded. These steps are inside the pipeline, so they are fitted on the training portion of each fold. The held-out fold does not set the medians, scales, or category vocabulary.

“ROC-AUC measures how well positive examples tend to rank above negative examples across thresholds. F1 combines precision and recall at the model's prediction threshold. Using both prevents a single accuracy number from hiding the class imbalance.”

**Show:** `replications/07_automl_model_search/artifacts/metrics.csv` and `model_comparison.png`.

“Histogram gradient boosting leads this comparison with mean ROC-AUC 0.9169 and mean F1 0.6988. Random forest's mean ROC-AUC is 0.9057; logistic regression's is 0.9014; extra trees' is 0.8869.

“This is a small AutoML-style search, not AutoGluon stacking or an exhaustive hyperparameter search. The same cross-validation scores selected the winner, so the winning score is selection evidence, not an independent final-test estimate. A stronger follow-up would lock the selected model and evaluate on untouched data or use nested cross-validation. I also should not rank these numbers directly against the original project's different train/test split as though the evaluation conditions were identical.”

**Understanding check:** Explain why fitting the encoder or imputer on the full dataset before cross-validation would leak information. Explain why choosing the best CV score introduces selection optimism.

## 6:15–9:15 — Forecasting with a chronological evaluation

**Show:** `replications/12_timeseries_forecasting/data/air_passengers.csv`, then `forecast_time_series`.

“The third addition uses AirPassengers, a series of 144 monthly international-airline passenger totals from 1949 through 1960, measured in thousands. It asks whether a simple regression model can improve on repeating last year's value for the same month.

“I sort the data chronologically and reserve the final twenty-four months for evaluation. Features are a time trend, sine and cosine encodings of month, the previous month's observation, and the observation twelve months earlier. Sine and cosine represent the calendar cycle without treating December and January as far apart.

“Ridge regression is fitted once on the earlier training rows. For each evaluation month, it predicts using the history that would be available immediately before that month. Later evaluation months therefore use actual observations from earlier evaluation months. This is a fixed-model rolling one-step evaluation across twenty-four months. It is not a twenty-four-month forecast generated from one starting date, and the model is not retrained each month.”

**Show:** `artifacts/forecast.png`, `artifacts/forecast.csv`, and `artifacts/metrics.json` in the forecasting directory.

“The seasonal-naive baseline uses the observed value twelve months earlier. Its mean absolute error is 47.583 thousand passengers and MAPE is 10.52 percent. Ridge's mean absolute error is 14.362 thousand passengers and MAPE is 3.15 percent under this same evaluation.

“MAE is in the original units. RMSE penalizes larger misses more heavily. MAPE divides each absolute error by the actual value and averages the fractions; the stored value 0.0315 is 3.15 percent. This series stays positive, but MAPE would be problematic around zero.

“Ridge with these features achieved lower error in this comparison. That does not establish that each feature caused the improvement or that the model will generalize to modern airline demand. A stronger follow-up would test multiple chronological windows and separately evaluate recursive forecasts if the goal is many months ahead without new observations.”

**Understanding check:** For the second held-out month, identify where its lag-one feature comes from. Explain why its true previous-month value is available for one-step prediction but unavailable for a fixed-origin multi-month forecast.

## 9:15–10:00 — Close with evidence and limitations

**Show:** the eight-test result and the six-experiment index.

“The tests check literal association counts, candidate coverage and finite CV metrics, chronological forecast behavior, and rejection of insufficient forecast history. The original pipeline tests also pass. Passing tests checks these behaviors; it is not proof of scientific validity or assignment completeness.

“Together, the original work and these additions cover six mapped experiment ideas. The repository contains the input provenance, implementation, output tables, figures, and explanations. The important result is that I can describe what each method measures and where its conclusions stop.”

## If replacing the original video instead of supplementing it

Prepend a short Part 1 and original-replication walkthrough:

1. Explain the Adult prediction question and CRISP-DM flow. State that the original UCI files were combined and re-split 80/20; do not describe this as the official UCI test partition.
2. Show the dummy baseline: 76.07% accuracy with zero positive-class recall. Contrast random forest's ROC-AUC 0.9170 and recall 0.8028 with logistic regression's recall 0.8370. Explain the precision/recall tradeoff. These models were compared on that same held-out split; there is no independent post-selection test.
3. Show clustering: four clusters chosen in advance, silhouette 0.2013 on 2,000 sampled records, uneven sizes. These exploratory fits use all numeric rows and do not prove natural demographic groups.
4. Explain Isolation Forest's 2,443 flagged rows. The 5% threshold was configured; the experiment does not know which records are true anomalies.
5. Show the audit: female-slice recall 0.6567 versus male-slice recall 0.8300. This is a limited descriptive diagnostic, not a complete fairness assessment. Feature importance is predictive association, not causation.
6. Continue with the three detailed scenes above.

## Publication checklist

- [x] Confirm selection of any six reference projects; retain adaptations 03, 04, 06, 07, 11, and 12.
- [ ] Rehearse the explanation and resolve anything you cannot explain independently.
- [ ] Record the supplement or a complete replacement walkthrough.
- [ ] Upload the video and verify it plays without your private account access.
- [ ] Replace the README's pending note with the actual video URL; keep the original link if using a supplement.
- [ ] Publish the reviewed implementation and documentation to the submitted repository's main branch.
- [ ] Open the Canvas submission's repository link and verify the grader can reach all final artifacts before September 9, 11:59 p.m. Pacific.
