# Results and Plain-Language Interpretation

## What was measured

The pipeline combined the UCI Adult training and test files, normalized whitespace and target labels, retained missing values for training-fold imputation, and made a stratified 80/20 split. Every classifier used the same leakage-safe preprocessing pipeline. The held-out test set contained 9,769 records.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Random forest | 0.8382 | 0.6263 | 0.8028 | 0.7037 | 0.9170 |
| Logistic regression | 0.8068 | 0.5651 | 0.8370 | 0.6747 | 0.9040 |
| Dummy baseline | 0.7607 | 0.0000 | 0.0000 | 0.0000 | 0.5000 |

## Paraphrase of the output

About 24% of the records belong to the `>50K` class, so accuracy alone is misleading. A model that always predicts `<=50K` is correct 76% of the time but never finds a high-income record. Both learned models clearly beat that baseline.

The random forest gave the best overall balance: it correctly ranked the two classes well (0.917 ROC-AUC) and found about 80% of the high-income records. Logistic regression found slightly more of that class—about 84%—but produced more false positives, lowering its precision and overall F1 score. The choice between them therefore depends on the cost of missed positives versus false alarms.

The random forest's largest impurity-based signals included age, marital-status/relationship categories, education level, capital gain, and hours worked. These are predictive associations in this historical dataset, not causal explanations.

## Replicated experiments

### Demographic clustering

MiniBatch K-means formed four groups from standardized numerical attributes. The sampled silhouette score was only **0.2013**, indicating substantial overlap rather than clean natural segments. Cluster sizes were also very uneven: 2,238; 25,036; 21,324; and 244 records. The honest conclusion is that this feature set does not support strong cluster claims without deeper feature design and stability analysis.

### Anomaly detection

Isolation Forest flagged 2,443 records. This is exactly 5% because the experiment set `contamination=0.05`; it is a ranking threshold chosen for demonstration, not evidence that precisely 5% of people are truly anomalous.

### Group diagnostic

For the selected random forest, the held-out sex slices were:

| Recorded sex | Rows | Accuracy | Recall for `>50K` |
|---|---:|---:|---:|
| Female | 3,289 | 0.9203 | 0.6567 |
| Male | 6,480 | 0.7965 | 0.8300 |

These descriptive slices expose a substantial recall difference. They do not establish fairness or unfairness by themselves, but they are enough to reject deployment without a purpose-specific fairness study, better data documentation, and stakeholder review.

## Recommendation

Use the random forest as the strongest educational benchmark and logistic regression as the interpretable comparison. Do not deploy either model for employment, lending, benefits, or another consequential decision. The dataset is historical, the target is an imperfect social proxy, sensitive attributes are present, and the observed group gap needs investigation.
