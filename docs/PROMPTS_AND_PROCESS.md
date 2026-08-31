# Prompts and Agent-Assisted Process

## Disclosure

This project was developed with OpenAI Codex as an agentic coding assistant. The assistant helped read the assignment sources, design the experiment, write tests and code, run the analysis, inspect generated figures, and draft the documentation. The author remains responsible for reviewing, understanding, recording, and submitting the work.

This is a process record, not a fabricated verbatim transcript. The original Codex task can be shared separately through the Codex app if the instructor requires the complete conversation.

## Source prompts reviewed

- Instructor assignment: [CMPE 255 Assignment 1, Fall 2026](https://docs.google.com/document/d/1NMl64CxIyq3BznMgAFotEsp0fHpEkQe4b7Oi98SEjaA/edit?tab=t.0)
- Instructor worked example: Adult Income analysis organized around CRISP-DM
- Reference prompt catalog: [`dlmastery/data_science_examples/PROMPTS.md`](https://github.com/dlmastery/data_science_examples/blob/main/PROMPTS.md)

The reference catalog contains 14 full-stack examples. This submission deliberately chose a focused replication of three data-science themes rather than copying the portfolio wholesale.

## Adapted master prompt

> Build a reproducible, end-to-end CRISP-DM project on the Adult/Census Income dataset. Include data understanding, validation, cleaning, leakage-safe preprocessing, a dummy baseline, logistic regression, random forest, appropriate classification metrics, clustering, anomaly detection, interpretable visual evidence, and a responsible-use audit. Use fixed random seeds, test the non-trivial data logic, generate all artifacts from one command, and explain weak or negative findings instead of overstating them.

## Reference-theme adaptations

1. **End-to-end prediction:** adapted the repository's supervised-learning prompts to Adult Income and added a dummy baseline so accuracy could be interpreted under class imbalance.
2. **Customer segmentation clustering:** adapted the clustering prompt to demographic numeric attributes using MiniBatch K-means and a sampled silhouette score.
3. **Anomaly detection:** adapted the anomaly-platform prompt to an Isolation Forest experiment and explicitly documented that the selected contamination rate controls the number flagged.
4. **Enterprise audit:** adapted the audit prompt into leakage checks, deterministic seeds, group metrics, data-age limitations, and a non-deployment recommendation.

## Agent journey

1. Read the live assignment Google Doc and its linked 8,000-line worked transcript.
2. Read the public reference repository's README and prompt catalog.
3. Selected Adult Income for continuity with the instructor example and verified both its UCI source and Kaggle publication.
4. Wrote tests before production code for file loading, schema rejection, cleaning, determinism, and artifact output.
5. Ran the test once to observe the intended missing-module failure, then implemented the analysis.
6. Ran the pipeline on all 48,842 records and inspected every generated figure.
7. Wrote the conclusions from the measured output, including weak clustering and group-level limitations.

## Useful follow-up prompts

- “Explain why the dummy model's 76% accuracy is misleading.”
- “Compare random forest and logistic regression when false negatives are costly.”
- “Audit this pipeline for preprocessing leakage.”
- “Explain why a low silhouette score should change the clustering conclusion.”
- “Identify which claims are associations rather than causal conclusions.”
