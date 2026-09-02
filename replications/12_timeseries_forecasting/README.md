# Replication 6: Time-Series Forecasting

**Reference:** Project 12, TimePulse Forecasting Engine.

The classic R `AirPassengers` series contains 144 monthly international-airline passenger totals from 1949–1960. The final 24 months are held out chronologically. Seasonal-naive predictions are compared with Ridge regression using trend, month seasonality, lag-1, and lag-12 features.

## Result

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Seasonal naive | 47.583 | 49.987 | 10.52% |
| Ridge | **14.362** | **18.334** | **3.15%** |

Ridge captured the rising trend while retaining seasonal information, substantially improving the held-out forecast.

## Evidence and source

- [Forecast metrics](artifacts/metrics.json)
- [Holdout predictions](artifacts/forecast.csv)
- [Forecast visualization](artifacts/forecast.png)
- [Committed dataset](data/air_passengers.csv)
- [Official R dataset documentation](https://rweb.stat.umn.edu/R/library/datasets/html/AirPassengers.html)
- Implementation: [`src/replications.py`](../../src/replications.py)
