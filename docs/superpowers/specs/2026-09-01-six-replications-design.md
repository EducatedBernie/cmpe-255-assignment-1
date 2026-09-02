# Six Part 2 Replications Design

## Goal

Make Part 2 satisfy the emailed minimum of six defensible project replications while keeping the existing Adult Income submission coherent and reproducible.

## Replication map

| Reference project | Local replication | Status |
|---|---|---|
| 03 Customer Segmentation | MiniBatch K-means demographic clustering | Existing |
| 04 Market Basket Mining | Frequent item-pair and association-rule mining | New |
| 06 Anomaly Detection | Isolation Forest on standardized demographics | Existing |
| 07 AutoML AutoGluon | Automated scikit-learn candidate benchmark | New |
| 11 Enterprise DS Audit | Leakage, reproducibility, and group diagnostics | Existing |
| 12 Time-Series Forecasting | Seasonal-naive and Ridge forecasts on AirPassengers | New |

## Architecture

`src/replications.py` contains three independently testable functions: `mine_association_rules`, `benchmark_models`, and `forecast_time_series`. Its command-line entry point loads the existing Adult files plus a committed 144-row AirPassengers CSV and generates CSV/JSON evidence and PNG figures inside the relevant replication directories.

`replications/README.md` is the grader-facing index. Six numbered subdirectories each contain a concise README; existing results link to root artifacts instead of copying data. New experiment directories own their generated evidence.

## Methods

Association mining treats selected Adult categorical values as items and counts single items and unordered pairs. It reports directional rules meeting explicit support and confidence thresholds. The feature set is fixed and small, so direct pair counting is clearer than adding `mlxtend`.

The AutoML replication applies the same leakage-safe preprocessing to four scikit-learn candidates and ranks three-fold cross-validation results by ROC-AUC. It is an AutoML-style benchmark, not a claim to reproduce AutoGluon's stacked ensemble internals.

Time-series forecasting uses the official R `AirPassengers` series. The final 24 months are held out chronologically. A seasonal-naive forecast is compared with Ridge regression using trend, month, lag-1, and lag-12 features.

## Verification

- Tests must fail before `src.replications` exists, then pass after implementation.
- All six replication directories must exist and contain clear mappings to the instructor repository.
- New metrics and figures must be reproducible from `python -m src.replications`.
- Root README must state exactly six replications and link the replication index.
- Existing Part 1 metrics and tests must remain unchanged.

## Submission caveat

The existing YouTube walkthrough predates the three additions. The repository will be complete, but the student needs a short supplemental walkthrough covering projects 04, 07, and 12 if the email requires every replication to appear on video.
