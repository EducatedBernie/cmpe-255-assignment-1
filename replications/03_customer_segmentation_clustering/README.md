# Replication 1: Customer Segmentation Clustering

**Reference:** Project 03, Customer Intelligence Clustering.

MiniBatch K-means grouped 48,842 Adult records into four clusters using standardized numerical attributes. The silhouette score was calculated on a fixed 2,000-row sample to keep the pairwise calculation bounded.

## Result

- Silhouette score: **0.2013**
- Cluster sizes: **2,238; 25,036; 21,324; 244**

The low silhouette and uneven sizes indicate overlapping demographics, not four clean customer segments. That negative result is the appropriate conclusion.

## Evidence

- [Cluster sizes](../../artifacts/cluster_sizes.csv)
- [Combined experiment summary](../../artifacts/summary.json)
- Implementation: [`src/analysis.py`](../../src/analysis.py)
