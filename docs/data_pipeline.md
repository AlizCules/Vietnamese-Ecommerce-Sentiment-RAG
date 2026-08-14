# Data Pipeline and Quality Control

The data layer prepares two related views: a labeled sentiment dataset and a larger review corpus for retrieval.

## Sentiment cleaning

The sentiment workflow applies Unicode normalization, HTML cleanup, whitespace normalization and duplicate-key normalization before modeling. Duplicate reviews are removed to reduce memorization and evaluation inflation. When duplicate keys carry conflicting labels, the conflicting rows are excluded rather than assigning an arbitrary label.

Verified counts from `data/reports/data_summary.json`:

| Stage | Rows |
| --- | ---: |
| Raw sentiment input | 5,971 |
| After deduplication | 5,162 |
| Conflicting duplicate rows removed | 46 |

The three classes are derived from ratings: 1–2 negative, 3 neutral, and 4–5 positive. The split is stratified by class into train, validation and test partitions. The exact class counts are stored in the same summary artifact.

## Retrieval preparation

The final retrieval corpus contains 82,677 documents. Empty comments and duplicate document/comment pairs are checked in the synchronized corpus summary. Category and rating distributions are retained as aggregate reports for analysis.

## Reproducibility boundaries

Cleaning and split logic are implemented in `src/module1_data_layer.py`; sentiment modeling is implemented in `src/module2_baseline_sentiment_classification.py`; retrieval preparation and indexing are implemented by the Module 4 scripts. Large embeddings and indexes are not rebuilt by lightweight CI.
