# Dataset

Running `python -m src.analysis` downloads these original UCI files into this directory:

- `adult.data`
- `adult.test`

They are ignored by Git because they are reproducibly fetched from the [UCI Adult dataset](https://archive.ics.uci.edu/dataset/2/adult). The same problem is published on Kaggle as [Income Predictor Dataset — US Adult](https://www.kaggle.com/datasets/jainaru/adult-income-census-dataset/data).

The combined dataset contains 48,842 records and 14 predictors. Its task is to classify whether annual income exceeds $50,000.
