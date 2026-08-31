# Beyond Accuracy: What an Agent-Assisted Adult Income Project Actually Taught Me

*Draft for Medium — add your name, course, and repository/video links before publishing.*

## The project

For this assignment I used an agentic coding assistant to build an end-to-end data-science study around the Adult, or Census Income, dataset. The dataset contains 48,842 records and 14 demographic and employment-related predictors. The classification goal is to estimate whether a record belongs to the annual-income-above-$50,000 class.

I chose this dataset for two reasons. First, it is a popular Kaggle learning problem with an authoritative source in the UCI Machine Learning Repository. Second, it matches the instructor's worked example, which let me focus on improving reproducibility and interpretation rather than simply choosing a different dataset.

The final workflow followed CRISP-DM: business understanding, data understanding, preparation, modeling, evaluation, and responsible interpretation. I also adapted three experiments from the instructor's reference prompt repository: clustering, anomaly detection, and a model audit.

## Why I started with a deliberately weak model

Only 23.93% of records are labeled above $50,000. That imbalance makes a dummy classifier surprisingly accurate: always predicting the majority class produces 76.07% accuracy. However, its recall and F1 score for the high-income class are both zero.

This baseline changed the meaning of the experiment. A learned model did not deserve praise merely for exceeding 76% accuracy. It needed to identify the minority class and rank cases meaningfully. That is why I reported precision, recall, F1, and ROC-AUC alongside accuracy.

## Comparing two useful models

The random forest produced 83.82% accuracy, 80.28% recall, a 0.7037 F1 score, and 0.917 ROC-AUC. Logistic regression reached 80.68% accuracy and 0.904 ROC-AUC. Its 83.70% recall was slightly higher than the forest's, but its lower precision reduced its F1 score to 0.6747.

The result is not “random forest wins” in every context. It is a trade-off. Logistic regression catches more positives but raises more false alarms. Random forest offers the stronger overall held-out balance. A real project would decide between them using the actual costs of false positives and false negatives.

All preprocessing was fitted inside scikit-learn pipelines after the train/test split. Numeric values used median imputation and standardization. Categorical values used most-frequent imputation and one-hot encoding. Keeping preprocessing inside the model pipeline prevents information from the held-out test set from leaking into training.

## Negative findings are still findings

I used MiniBatch K-means to explore four demographic clusters. The sampled silhouette score was only 0.2013, and one cluster contained just 244 records while two contained more than 20,000 each. Those numbers do not support a story about four clean population segments. The appropriate conclusion is that the selected numerical feature space overlaps heavily and needs stronger feature design and stability tests before segmentation claims are made.

Isolation Forest flagged 2,443 records, or 5%. That number also needs careful wording. I configured the model with a 5% contamination threshold, so the experiment ranks unusual records and then cuts at a chosen point. It did not independently discover that exactly 5% of the population is anomalous.

## The audit changed the recommendation

The selected random forest reached 92.03% accuracy for records marked female and 79.65% for records marked male. Yet recall for the above-$50,000 class moved in the opposite direction: 65.67% for the female slice and 83.00% for the male slice.

These numbers do not prove that the model meets or violates a particular fairness definition. They do show that a single aggregate score hides important behavior. The data is also based on 1994 census-era patterns, includes sensitive demographic fields, and uses income as a socially loaded target.

For those reasons, my recommendation is educational use only. The model is useful for learning preprocessing, baselines, model comparison, and auditing. It is not suitable for employment, lending, benefits, or another consequential decision.

## What the coding agent changed—and what it did not

The agent accelerated repetitive work: reading the assignment sources, creating the pipeline, running tests, generating artifacts, and checking figures. It also helped preserve a disciplined workflow by writing a failing test before implementation and grounding the narrative in generated metrics.

The agent did not remove the need for judgment. I still needed to decide what question was defensible, which metrics mattered, whether clustering was meaningful, and how to describe sensitive group differences. The best result of agent-assisted data science was not more code. It was a faster path to evidence that I could inspect, challenge, and explain.

## Reproducibility

The public repository contains the analysis code, tests, generated metrics, figures, prompt/process record, and video walkthrough. A fresh run creates a local environment, downloads the original UCI files, and regenerates the artifacts with a fixed random seed.
