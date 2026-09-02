"""Three focused experiment replications for CMPE 255 Assignment 1, Part 2."""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.analysis import NUMERIC_COLUMNS, RANDOM_STATE, clean_adult, load_adult


def mine_association_rules(
    frame: pd.DataFrame, min_support: float = 0.08, min_confidence: float = 0.6
) -> pd.DataFrame:
    """Mine directional single-item association rules from selected Adult columns."""
    columns = ["education", "occupation", "marital-status", "income"]
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")
    if not 0 < min_support <= 1 or not 0 < min_confidence <= 1:
        raise ValueError("support and confidence must be in (0, 1]")

    single_counts: Counter[str] = Counter()
    pair_counts: Counter[tuple[str, str]] = Counter()
    for _, row in frame[columns].iterrows():
        items = sorted(
            f"{column}={row[column]}" for column in columns if pd.notna(row[column])
        )
        single_counts.update(items)
        pair_counts.update(combinations(items, 2))

    total = len(frame)
    rules = []
    for (left, right), pair_count in pair_counts.items():
        support = pair_count / total
        if support < min_support:
            continue
        for antecedent, consequent in ((left, right), (right, left)):
            confidence = pair_count / single_counts[antecedent]
            if confidence < min_confidence:
                continue
            consequent_support = single_counts[consequent] / total
            rules.append(
                {
                    "antecedent": antecedent,
                    "consequent": consequent,
                    "support": round(support, 6),
                    "confidence": round(confidence, 6),
                    "lift": round(confidence / consequent_support, 6),
                    "rows": pair_count,
                }
            )
    columns_out = ["antecedent", "consequent", "support", "confidence", "lift", "rows"]
    if not rules:
        return pd.DataFrame(columns=columns_out)
    return (
        pd.DataFrame(rules, columns=columns_out)
        .sort_values(["lift", "confidence", "support", "antecedent"], ascending=[False, False, False, True])
        .reset_index(drop=True)
    )


def benchmark_models(frame: pd.DataFrame, max_rows: int = 12_000) -> pd.DataFrame:
    """Run a small deterministic AutoML-style benchmark over four classifiers."""
    data = clean_adult(frame)
    if max_rows < 30:
        raise ValueError("max_rows must be at least 30")
    if len(data) > max_rows:
        data = data.sample(max_rows, random_state=RANDOM_STATE)

    features = data.drop(columns="income")
    target = data["income"].eq(">50K").astype(int)
    categorical_columns = [column for column in features if column not in NUMERIC_COLUMNS]
    preprocessor = ColumnTransformer(
        [
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                NUMERIC_COLUMNS,
            ),
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "onehot",
                            OneHotEncoder(handle_unknown="ignore", min_frequency=2, sparse_output=False),
                        ),
                    ]
                ),
                categorical_columns,
            ),
        ]
    )
    candidates = {
        "Logistic regression": LogisticRegression(
            max_iter=1_000, class_weight="balanced", random_state=RANDOM_STATE
        ),
        "Random forest": RandomForestClassifier(
            n_estimators=80,
            min_samples_leaf=2,
            class_weight="balanced_subsample",
            n_jobs=1,
            random_state=RANDOM_STATE,
        ),
        "Extra trees": ExtraTreesClassifier(
            n_estimators=80,
            min_samples_leaf=2,
            class_weight="balanced",
            n_jobs=1,
            random_state=RANDOM_STATE,
        ),
        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=80, l2_regularization=1.0, random_state=RANDOM_STATE
        ),
    }
    folds = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)
    rows = []
    for name, candidate in candidates.items():
        scores = cross_validate(
            Pipeline([("preprocess", preprocessor), ("model", candidate)]),
            features,
            target,
            cv=folds,
            scoring={"roc_auc": "roc_auc", "f1": "f1"},
            error_score="raise",
            n_jobs=1,
        )
        rows.append(
            {
                "model": name,
                "roc_auc_mean": round(float(scores["test_roc_auc"].mean()), 4),
                "roc_auc_std": round(float(scores["test_roc_auc"].std()), 4),
                "f1_mean": round(float(scores["test_f1"].mean()), 4),
                "f1_std": round(float(scores["test_f1"].std()), 4),
                "rows": len(data),
                "folds": 3,
            }
        )
    return pd.DataFrame(rows).sort_values("roc_auc_mean", ascending=False).reset_index(drop=True)


def forecast_time_series(
    frame: pd.DataFrame, test_months: int = 24
) -> tuple[dict[str, dict[str, float]], pd.DataFrame]:
    """Compare seasonal-naive and Ridge forecasts on a chronological holdout."""
    required = {"date", "passengers"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")
    minimum_rows = test_months + 13
    if test_months < 1 or len(frame) < minimum_rows:
        raise ValueError(f"time series needs at least {minimum_rows} rows")

    data = frame[["date", "passengers"]].copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    data["passengers"] = pd.to_numeric(data["passengers"], errors="raise")
    data = data.sort_values("date").reset_index(drop=True)
    data["trend"] = np.arange(len(data))
    data["month_sin"] = np.sin(2 * np.pi * data["date"].dt.month / 12)
    data["month_cos"] = np.cos(2 * np.pi * data["date"].dt.month / 12)
    data["lag_1"] = data["passengers"].shift(1)
    data["lag_12"] = data["passengers"].shift(12)
    supervised = data.dropna().reset_index(drop=True)
    train = supervised.iloc[:-test_months]
    test = supervised.iloc[-test_months:]
    if train.empty:
        raise ValueError(f"time series needs at least {minimum_rows} rows")

    feature_columns = ["trend", "month_sin", "month_cos", "lag_1", "lag_12"]
    model = Ridge(alpha=1.0).fit(train[feature_columns], train["passengers"])
    ridge_prediction = model.predict(test[feature_columns])
    actual = test["passengers"].to_numpy()
    seasonal_prediction = test["lag_12"].to_numpy()

    def metrics(prediction: np.ndarray) -> dict[str, float]:
        return {
            "mae": round(float(mean_absolute_error(actual, prediction)), 3),
            "rmse": round(float(np.sqrt(mean_squared_error(actual, prediction))), 3),
            "mape": round(float(mean_absolute_percentage_error(actual, prediction)), 4),
        }

    forecast = pd.DataFrame(
        {
            "date": test["date"].to_numpy(),
            "actual": actual,
            "seasonal_naive": seasonal_prediction,
            "ridge": np.round(ridge_prediction, 3),
        }
    )
    return {"seasonal_naive": metrics(seasonal_prediction), "ridge": metrics(ridge_prediction)}, forecast


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[1]
    adult = load_adult(repository / "data")

    association_dir = repository / "replications/04_associative_pattern_mining/artifacts"
    automl_dir = repository / "replications/07_automl_model_search/artifacts"
    forecast_dir = repository / "replications/12_timeseries_forecasting/artifacts"
    for directory in (association_dir, automl_dir, forecast_dir):
        directory.mkdir(parents=True, exist_ok=True)

    rules = mine_association_rules(clean_adult(adult))
    rules.to_csv(association_dir / "rules.csv", index=False)
    top_rules = rules.head(12).sort_values("lift")
    plt.figure(figsize=(9, 5))
    labels = top_rules["antecedent"] + " → " + top_rules["consequent"]
    plt.barh(labels, top_rules["lift"], color="#7c3aed")
    plt.xlabel("Lift")
    plt.title("Top Adult Income Association Rules")
    plt.tight_layout()
    plt.savefig(association_dir / "top_rules.png", dpi=160)
    plt.close()

    benchmark = benchmark_models(adult)
    benchmark.to_csv(automl_dir / "metrics.csv", index=False)
    plt.figure(figsize=(8, 4.5))
    benchmark.set_index("model")[["roc_auc_mean", "f1_mean"]].plot.bar(
        ax=plt.gca(), ylim=(0, 1), color=["#2563eb", "#10b981"]
    )
    plt.ylabel("Three-fold CV score")
    plt.title("AutoML-Style Candidate Benchmark")
    plt.xticks(rotation=12, ha="right")
    plt.tight_layout()
    plt.savefig(automl_dir / "model_comparison.png", dpi=160)
    plt.close()

    air = pd.read_csv(repository / "replications/12_timeseries_forecasting/data/air_passengers.csv")
    forecast_metrics, forecast = forecast_time_series(air)
    (forecast_dir / "metrics.json").write_text(json.dumps(forecast_metrics, indent=2) + "\n")
    forecast.to_csv(forecast_dir / "forecast.csv", index=False)
    plt.figure(figsize=(9, 4.5))
    plt.plot(forecast["date"], forecast["actual"], label="Actual", color="#111827", linewidth=2)
    plt.plot(forecast["date"], forecast["seasonal_naive"], label="Seasonal naive", linestyle="--")
    plt.plot(forecast["date"], forecast["ridge"], label="Ridge", linestyle=":")
    plt.title("AirPassengers: Final 24-Month Holdout")
    plt.ylabel("Passengers (thousands)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(forecast_dir / "forecast.png", dpi=160)
    plt.close()

    print(
        json.dumps(
            {
                "association_rules": len(rules),
                "automl_best_model": benchmark.iloc[0]["model"],
                "automl_best_roc_auc": benchmark.iloc[0]["roc_auc_mean"],
                "forecast_metrics": forecast_metrics,
            },
            indent=2,
        )
    )
