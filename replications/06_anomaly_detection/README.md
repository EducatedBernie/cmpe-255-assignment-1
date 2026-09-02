# Replication 3: Anomaly Detection

**Reference:** Project 06, Anomaly Threat Intelligence.

Isolation Forest ranked unusual combinations of standardized Adult numerical attributes.

## Result

- Flagged rows: **2,443**
- Flagged rate: **5%**

The 5% rate is controlled by `contamination=0.05`; it is a demonstration threshold, not evidence that exactly 5% of people are objectively anomalous.

## Evidence

- [Combined experiment summary](../../artifacts/summary.json)
- Implementation: [`src/analysis.py`](../../src/analysis.py)
