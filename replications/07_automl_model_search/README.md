# Replication 4: AutoML-Style Model Search

**Reference:** Project 07, AutoML AutoGluon Stacking.

This compact AutoML-style benchmark applies identical leakage-safe preprocessing to four scikit-learn candidates and ranks three-fold cross-validation results on a fixed 12,000-row Adult sample. It demonstrates automated candidate comparison without claiming AutoGluon stacking parity.

## Result

| Candidate | ROC-AUC | F1 |
|---|---:|---:|
| HistGradientBoosting | **0.9169** | **0.6988** |
| Random forest | 0.9057 | 0.6938 |
| Logistic regression | 0.9014 | 0.6742 |
| Extra trees | 0.8869 | 0.6535 |

The winner is selected using these same cross-validation scores. Its score is not an independent final-test estimate; use an untouched test set or nested cross-validation for that claim.

## Evidence

- [Cross-validation metrics](artifacts/metrics.csv)
- [Candidate comparison](artifacts/model_comparison.png)
- Implementation: [`src/replications.py`](../../src/replications.py)
