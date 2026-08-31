"""Reproducible CRISP-DM analysis of the Adult/Census Income dataset."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import MiniBatchKMeans
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    silhouette_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
COLUMNS = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
    "income",
]
NUMERIC_COLUMNS = [
    "age",
    "fnlwgt",
    "education-num",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
]
DATA_URLS = {
    "adult.data": "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
    "adult.test": "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test",
}


def load_adult(data_dir: Path) -> pd.DataFrame:
    """Load the standard UCI train and test files from ``data_dir``."""
    frames = []
    for filename in DATA_URLS:
        path = data_dir / filename
        if not path.is_file():
            raise FileNotFoundError(f"missing dataset file: {path}")
        frames.append(
            pd.read_csv(
                path,
                names=COLUMNS,
                header=None,
                comment="|",
                skipinitialspace=True,
                na_values=["?"],
            )
        )
    return pd.concat(frames, ignore_index=True)


def clean_adult(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate and normalize Adult data without fitting preprocessing state."""
    missing = sorted(set(COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")

    cleaned = frame[COLUMNS].copy()
    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column] = cleaned[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
        cleaned[column] = cleaned[column].replace("?", np.nan)
    cleaned["income"] = cleaned["income"].str.rstrip(".")

    labels = set(cleaned["income"].dropna().unique())
    expected = {"<=50K", ">50K"}
    if not labels or not labels.issubset(expected):
        raise ValueError(f"unexpected income labels: {sorted(labels)}")
    return cleaned.dropna(subset=["income"]).reset_index(drop=True)


def run_analysis(frame: pd.DataFrame, output_dir: Path) -> dict:
    """Run classification, clustering, and anomaly experiments and save evidence."""
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(exist_ok=True)

    data = clean_adult(frame)
    features = data.drop(columns="income")
    target = data["income"].eq(">50K").astype(int)
    categorical_columns = [column for column in features if column not in NUMERIC_COLUMNS]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=target,
    )
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
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_columns,
            ),
        ]
    )
    models = {
        "Dummy baseline": DummyClassifier(strategy="most_frequent"),
        "Logistic regression": LogisticRegression(
            max_iter=1_000,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "Random forest": RandomForestClassifier(
            n_estimators=120,
            min_samples_leaf=2,
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        ),
    }

    rows = []
    fitted = {}
    predictions = {}
    for name, model in models.items():
        pipeline = Pipeline([("preprocess", preprocessor), ("model", model)])
        pipeline.fit(x_train, y_train)
        predicted = pipeline.predict(x_test)
        probability = pipeline.predict_proba(x_test)[:, 1]
        fitted[name] = pipeline
        predictions[name] = predicted
        rows.append(
            {
                "model": name,
                "accuracy": round(float(accuracy_score(y_test, predicted)), 4),
                "precision": round(float(precision_score(y_test, predicted, zero_division=0)), 4),
                "recall": round(float(recall_score(y_test, predicted, zero_division=0)), 4),
                "f1": round(float(f1_score(y_test, predicted, zero_division=0)), 4),
                "roc_auc": round(float(roc_auc_score(y_test, probability)), 4),
            }
        )

    metrics = pd.DataFrame(rows).sort_values("roc_auc", ascending=False).reset_index(drop=True)
    metrics.to_csv(output_dir / "metrics.csv", index=False)
    best_model = str(metrics.iloc[0]["model"])

    group_rows = []
    evaluation = x_test[["sex"]].copy()
    evaluation["actual"] = y_test
    evaluation["predicted"] = predictions[best_model]
    for group, subset in evaluation.groupby("sex", dropna=False):
        if len(subset) < 2:
            continue
        group_rows.append(
            {
                "sex": "Missing" if pd.isna(group) else str(group),
                "rows": int(len(subset)),
                "accuracy": round(float(accuracy_score(subset["actual"], subset["predicted"])), 4),
                "recall": round(
                    float(recall_score(subset["actual"], subset["predicted"], zero_division=0)), 4
                ),
            }
        )
    pd.DataFrame(group_rows).to_csv(output_dir / "group_metrics.csv", index=False)

    numeric = data[NUMERIC_COLUMNS].copy()
    numeric = numeric.fillna(numeric.median(numeric_only=True))
    scaled_numeric = StandardScaler().fit_transform(numeric)
    clusters = MiniBatchKMeans(
        n_clusters=4,
        batch_size=min(1_024, len(data)),
        n_init=10,
        random_state=RANDOM_STATE,
    ).fit_predict(scaled_numeric)
    sample_size = min(2_000, len(data))
    rng = np.random.default_rng(RANDOM_STATE)
    sample = np.sort(rng.choice(len(data), size=sample_size, replace=False))
    sampled_labels = clusters[sample]
    silhouette = (
        float(silhouette_score(scaled_numeric[sample], sampled_labels))
        if len(set(sampled_labels)) > 1
        else None
    )
    cluster_sizes = pd.Series(clusters).value_counts().sort_index()
    cluster_sizes.rename_axis("cluster").rename("rows").to_csv(output_dir / "cluster_sizes.csv")

    anomalies = IsolationForest(contamination=0.05, random_state=RANDOM_STATE).fit_predict(
        scaled_numeric
    )
    anomaly_count = int((anomalies == -1).sum())

    plt.figure(figsize=(7, 4))
    income_counts = data["income"].value_counts().reindex(["<=50K", ">50K"])
    income_counts.plot.bar(color=["#2563eb", "#f59e0b"])
    plt.title("Adult Income Class Distribution")
    plt.xlabel("Income class")
    plt.ylabel("Records")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(figures_dir / "income_distribution.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 4.5))
    plot_metrics = metrics.set_index("model")[["accuracy", "recall", "f1", "roc_auc"]]
    plot_metrics.plot.bar(ax=plt.gca(), ylim=(0, 1), color=["#2563eb", "#f59e0b", "#10b981", "#7c3aed"])
    plt.title("Held-out Classification Performance")
    plt.ylabel("Score")
    plt.xticks(rotation=12, ha="right")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(figures_dir / "model_comparison.png", dpi=160)
    plt.close()

    forest = fitted["Random forest"]
    feature_names = forest.named_steps["preprocess"].get_feature_names_out()
    importances = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": forest.named_steps["model"].feature_importances_,
        }
    ).sort_values("importance", ascending=False)
    importances.head(20).to_csv(output_dir / "feature_importance.csv", index=False)
    top = importances.head(12).sort_values("importance")
    plt.figure(figsize=(8, 5))
    plt.barh(top["feature"].str.replace(r"^[^_]+__", "", regex=True), top["importance"], color="#2563eb")
    plt.title("Random Forest: Top Feature Importances")
    plt.xlabel("Mean decrease in impurity")
    plt.tight_layout()
    plt.savefig(figures_dir / "feature_importance.png", dpi=160)
    plt.close()

    summary = {
        "rows": int(len(data)),
        "features": int(features.shape[1]),
        "positive_rate": round(float(target.mean()), 4),
        "missing_cells": int(data.isna().sum().sum()),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "classification": metrics.to_dict(orient="records"),
        "best_model": best_model,
        "clustering": {
            "clusters": 4,
            "silhouette_sample_rows": sample_size,
            "silhouette": None if silhouette is None else round(silhouette, 4),
            "sizes": {str(key): int(value) for key, value in cluster_sizes.items()},
        },
        "anomaly_detection": {
            "method": "IsolationForest",
            "flagged_rows": anomaly_count,
            "flagged_rate": round(anomaly_count / len(data), 4),
        },
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[1]
    data_directory = repository / "data"
    data_directory.mkdir(exist_ok=True)
    for filename, url in DATA_URLS.items():
        destination = data_directory / filename
        if destination.is_file():
            continue
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                temporary.write_bytes(response.read())
            temporary.replace(destination)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise

    result = run_analysis(load_adult(data_directory), repository / "artifacts")
    print(json.dumps(result, indent=2))
