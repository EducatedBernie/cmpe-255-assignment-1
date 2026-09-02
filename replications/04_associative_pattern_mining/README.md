# Replication 2: Associative Pattern Mining

**Reference:** Project 04, Market Basket Pattern Mining.

Each Adult record becomes a small basket of education, occupation, marital-status, and income items. Direct pair counting produces directional rules with support, confidence, and lift; no extra mining dependency is required for this fixed four-item basket.

## Result

Nine rules met support ≥ 8% and confidence ≥ 60%. The strongest rule was:

`income=>50K → marital-status=Married-civ-spouse`

- Support: **20.44%**
- Confidence: **85.43%**
- Lift: **1.8645**

These are historical associations, not causal or prescriptive relationships.

## Evidence

- [All rules](artifacts/rules.csv)
- [Rule-lift visualization](artifacts/top_rules.png)
- Implementation: [`src/replications.py`](../../src/replications.py)
