# Replication 6: Time-Series Forecasting

**Reference:** Project 12, TimePulse Forecasting Engine.

The classic R `AirPassengers` series contains 144 monthly international-airline passenger totals from 1949–1960. The final 24 months are evaluated chronologically as **fixed-model rolling one-step predictions**. Seasonal-naive predictions are compared with Ridge regression using trend, month seasonality, lag-1, and lag-12 features. Later evaluation rows use actual earlier observations from the holdout period. This is not a 24-month forecast made from one fixed origin, and Ridge is not refitted each month.

## Result

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Seasonal naive | 47.583 | 49.987 | 10.52% |
| Ridge | **14.362** | **18.334** | **3.15%** |

Ridge with these features achieved lower error under this evaluation. This comparison does not isolate the contribution of each feature or establish performance on other time periods.

## Evidence and source

- [Forecast metrics](artifacts/metrics.json)
- [Holdout predictions](artifacts/forecast.csv)
- [Forecast visualization](artifacts/forecast.png)
- [Committed dataset](data/air_passengers.csv)
- [Official R dataset documentation](https://rweb.stat.umn.edu/R/library/datasets/html/AirPassengers.html)
- Implementation: [`src/replications.py`](../../src/replications.py)
