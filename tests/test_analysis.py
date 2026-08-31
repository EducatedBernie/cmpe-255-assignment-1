import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.analysis import COLUMNS, clean_adult, load_adult, run_analysis


def adult_fixture(rows: int = 80) -> pd.DataFrame:
    records = []
    for index in range(rows):
        high_income = index % 4 == 0
        records.append(
            [
                25 + index % 35,
                " Private" if index % 7 else " ?",
                100_000 + index * 101,
                " Bachelors" if high_income else " HS-grad",
                13 if high_income else 9,
                " Married-civ-spouse" if high_income else " Never-married",
                " Exec-managerial" if high_income else " Sales",
                " Husband" if high_income else " Not-in-family",
                " White",
                " Male" if index % 2 else " Female",
                5_000 if high_income else 0,
                0,
                45 if high_income else 35,
                " United-States",
                " >50K." if high_income else " <=50K.",
            ]
        )
    return pd.DataFrame(records, columns=COLUMNS)


class CleanAdultTests(unittest.TestCase):
    def test_loads_train_and_test_files_while_ignoring_test_comment(self):
        first = ", ".join(map(str, adult_fixture(1).iloc[0].tolist()))
        second = ", ".join(map(str, adult_fixture(2).iloc[1].tolist()))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "adult.data").write_text(first + "\n")
            (path / "adult.test").write_text("| test header\n" + second + "\n")

            loaded = load_adult(path)

        self.assertEqual(len(loaded), 2)
        self.assertEqual(list(loaded.columns), COLUMNS)

    def test_rejects_missing_required_column(self):
        with self.assertRaisesRegex(ValueError, "missing columns"):
            clean_adult(adult_fixture().drop(columns=["age"]))

    def test_normalizes_missing_markers_and_target_punctuation(self):
        cleaned = clean_adult(adult_fixture())

        self.assertTrue(cleaned["workclass"].isna().any())
        self.assertEqual(set(cleaned["income"]), {"<=50K", ">50K"})
        self.assertFalse(cleaned.select_dtypes("object").apply(lambda col: col.str.startswith(" ").any()).any())


class RunAnalysisTests(unittest.TestCase):
    def test_writes_deterministic_metrics_and_summary(self):
        frame = clean_adult(adult_fixture())
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            result_one = run_analysis(frame, Path(first))
            result_two = run_analysis(frame, Path(second))

            self.assertEqual(result_one["classification"], result_two["classification"])
            self.assertEqual(
                {row["model"] for row in result_one["classification"]},
                {"Dummy baseline", "Logistic regression", "Random forest"},
            )
            self.assertEqual(result_one["rows"], 80)
            self.assertTrue((Path(first) / "metrics.csv").is_file())
            self.assertTrue((Path(first) / "summary.json").is_file())
            self.assertTrue((Path(first) / "figures" / "model_comparison.png").is_file())
            self.assertEqual(json.loads((Path(first) / "summary.json").read_text())["rows"], 80)


if __name__ == "__main__":
    unittest.main()
