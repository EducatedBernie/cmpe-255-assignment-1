# Part 2 — Six Creative Project Replications

This directory maps six reproducible experiments to the instructor's [`data_science_examples`](https://github.com/dlmastery/data_science_examples) prompt catalog. Each replication keeps the reference project's core data-science idea while using a smaller, auditable implementation suitable for one assignment repository.

| # | Reference project | Local evidence | Key result |
|---:|---|---|---|
| 1 | [03 Customer Segmentation](03_customer_segmentation_clustering/) | MiniBatch K-means and cluster sizes | Silhouette 0.2013; weak separation |
| 2 | [04 Associative Pattern Mining](04_associative_pattern_mining/) | Nine support/confidence/lift rules | Top lift 1.8645 |
| 3 | [06 Anomaly Detection](06_anomaly_detection/) | Isolation Forest ranking | 2,443 rows at configured 5% cutoff |
| 4 | [07 AutoML](07_automl_model_search/) | Four-candidate, three-fold benchmark | Best ROC-AUC 0.9169 |
| 5 | [11 Enterprise DS Audit](11_enterprise_ds_audit/) | Leakage, reproducibility, and group checks | Material recall gap identified |
| 6 | [12 Time-Series Forecasting](12_timeseries_forecasting/) | Seasonal-naive versus Ridge | Ridge holdout MAPE 3.15% |

## Reproduce everything

From the repository root:

```bash
python -m src.analysis
python -m src.replications
python -m unittest discover -s tests -v
```

The existing YouTube walkthrough covers replications 03, 06, and 11. A short supplemental walkthrough is still needed for the new 04, 07, and 12 experiments if every replication must appear on video.
