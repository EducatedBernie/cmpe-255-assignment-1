import unittest

import numpy as np
import pandas as pd

from src.analysis import COLUMNS
from src.replications import benchmark_models, forecast_time_series, mine_association_rules


def adult_fixture(rows: int = 80) -> pd.DataFrame:
    records = []
    for index in range(rows):
        high_income = index % 4 == 0
        records.append(
            [
                24 + index % 40,
                "Private",
                90_000 + index * 113,
                "Bachelors" if high_income else "HS-grad",
                13 if high_income else 9,
                "Married-civ-spouse" if high_income else "Never-married",
                "Exec-managerial" if high_income else "Sales",
                "Husband" if high_income else "Not-in-family",
                "White",
                "Male" if index % 2 else "Female",
                4_500 if high_income else 0,
                0,
                45 if high_income else 35,
                "United-States",
                ">50K" if high_income else "<=50K",
            ]
        )
    return pd.DataFrame(records, columns=COLUMNS)


class AssociationRuleTests(unittest.TestCase):
    def test_reports_support_confidence_and_lift_from_literal_counts(self):
        frame = pd.DataFrame(
            {
                "education": ["Bachelors", "Bachelors", "HS-grad", "HS-grad"],
                "occupation": ["Exec-managerial", "Exec-managerial", "Sales", "Sales"],
                "marital-status": ["Married", "Married", "Single", "Single"],
                "income": [">50K", ">50K", "<=50K", "<=50K"],
            }
        )

        rules = mine_association_rules(frame, min_support=0.5, min_confidence=0.8)
        rule = rules[
            (rules["antecedent"] == "education=Bachelors")
            & (rules["consequent"] == "income=>50K")
        ].iloc[0]

        self.assertEqual(rule["support"], 0.5)
        self.assertEqual(rule["confidence"], 1.0)
        self.assertEqual(rule["lift"], 2.0)


class AutoMLBenchmarkTests(unittest.TestCase):
    def test_compares_four_candidates_with_finite_cross_validation_metrics(self):
        metrics = benchmark_models(adult_fixture(), max_rows=80)

        self.assertEqual(
            set(metrics["model"]),
            {"Logistic regression", "Random forest", "Extra trees", "HistGradientBoosting"},
        )
        self.assertTrue(np.isfinite(metrics[["roc_auc_mean", "f1_mean"]]).all().all())
        self.assertTrue(metrics["roc_auc_mean"].between(0, 1).all())


class ForecastTests(unittest.TestCase):
    def test_holds_out_final_months_and_uses_prior_year_for_seasonal_naive(self):
        dates = pd.date_range("2020-01-01", periods=36, freq="MS")
        passengers = np.array([100 + 2 * index + 10 * (index % 12) for index in range(36)])
        frame = pd.DataFrame({"date": dates, "passengers": passengers})

        metrics, forecast = forecast_time_series(frame, test_months=12)

        self.assertEqual(len(forecast), 12)
        self.assertEqual(forecast.iloc[0]["date"], dates[-12])
        self.assertEqual(forecast.iloc[0]["seasonal_naive"], passengers[-24])
        self.assertEqual(set(metrics), {"seasonal_naive", "ridge"})
        self.assertTrue(all(value >= 0 for model in metrics.values() for value in model.values()))

    def test_rejects_series_without_training_and_holdout_history(self):
        frame = pd.DataFrame(
            {"date": pd.date_range("2024-01-01", periods=20, freq="MS"), "passengers": range(20)}
        )

        with self.assertRaisesRegex(ValueError, "at least"):
            forecast_time_series(frame, test_months=12)


if __name__ == "__main__":
    unittest.main()
