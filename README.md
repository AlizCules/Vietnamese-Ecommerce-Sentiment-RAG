# Vietnamese E-commerce Review Analytics & RAG

An end-to-end text analytics project for Vietnamese e-commerce reviews. The repository covers data cleaning, descriptive review analysis, rating-derived sentiment classification, evidence retrieval, and a lightweight analytical web demo.

## Project at a Glance

| Raw sentiment reviews | Deduplicated reviews | Retrieval documents | Test Macro-F1 |
| ---: | ---: | ---: | ---: |
| 5,971 | 5,162 | 82,677 | **0.910** |

| Core stack | Sentiment model | Retrieval layer | Delivery layer |
| --- | --- | --- | --- |
| Python, pandas | TF-IDF + Linear SVM | multilingual embeddings + FAISS | FastAPI + HTML/CSS/JavaScript |

The main analytical flow is:

`Project-provided data → data quality → review analytics → sentiment classification → evidence retrieval → evaluation → analytical web demo`

## Analytical Objectives

- Establish a reproducible cleaning and quality-control process for Vietnamese review data.
- Describe sentiment, review length, rating and category composition using aggregate artifacts.
- Measure how well review text predicts rating-derived three-class sentiment labels.
- Retrieve relevant review evidence for operational questions such as delivery, packaging and product quality.
- Provide a small browser-based interface for inspecting predictions, evidence and metrics.

## Data and Label Definition

The repository uses project-provided Vietnamese e-commerce review files. The tracked material does not establish a verified public URL, license or original publisher; the provenance and redistribution status are documented in [`docs/data_sources.md`](docs/data_sources.md).

The supervised sentiment label is derived from the star rating rather than independently annotated from review text:

- ratings 1–2 → `negative`
- rating 3 → `neutral`
- ratings 4–5 → `positive`

Therefore, the classifier measures how well review text predicts these rating-derived classes. A Macro-F1 of 0.910 should not be interpreted as agreement with an independent human sentiment annotation set.

## Data Cleaning and Quality

The sentiment data layer applies Unicode normalization, HTML and whitespace cleanup, duplicate normalization, and conflict handling before the split. The verified counts are:

- 5,971 raw sentiment rows;
- 5,162 rows after deduplication;
- 46 conflicting duplicate rows removed;
- three-class distribution: 2,217 positive, 2,074 negative and 871 neutral.

The train, validation and test partitions are stratified by class. Duplicate removal is important because repeated reviews can inflate evaluation or allow a model to memorize text instead of learning generalizable patterns. The complete pipeline description is in [`docs/data_pipeline.md`](docs/data_pipeline.md).

## Review Analytics

The descriptive analysis is positioned before the NLP and retrieval extensions. The three-class distribution is 42.95% positive, 40.18% negative and 16.87% neutral. The repository also contains aggregate views of review length, rating composition and retrieval-corpus categories.

![Three-class sentiment distribution](figures/module3/sentiment_3class_distribution.png)

![Review text length distribution](figures/module3/sentiment_text_length_distribution.png)

![Retrieval corpus category distribution](figures/module3/rag_category_distribution.png)

The corresponding aggregate table is [`results/module3/overall_sentiment_distribution.csv`](results/module3/overall_sentiment_distribution.csv). Rating-versus-sentiment agreement is not presented as an independent insight because the three-class labels are constructed directly from ratings. Further analytical notes are available in [`docs/review_analytics.md`](docs/review_analytics.md).

## Sentiment Classification

Candidate models use TF-IDF features with unigram and bigram representations. Hyperparameters are selected using validation Macro-F1; the test set is evaluated only after the configuration has been selected.

| Model | Test Macro-F1 | Test Accuracy |
| --- | ---: | ---: |
| Majority baseline | 0.200 | 0.430 |
| TF-IDF + Logistic Regression | 0.894 | 0.917 |
| **TF-IDF + Linear SVM** | **0.910** | **0.933** |

The Linear SVM is the selected model by validation Macro-F1. Its neutral-class F1 is approximately 0.823, lower than the negative and positive classes. Existing error-analysis artifacts show short or ambiguous reviews among the difficult cases; these observations are discussed without changing the benchmark. See [`docs/sentiment_model.md`](docs/sentiment_model.md).

## Evidence Retrieval and RAG

The retrieval component is an evidence-grounded review search and answer-generation layer:

`Query → Vietnamese query expansion → dense FAISS retrieval → optional metadata filtering → evidence selection → template-based answer generation`

The final corpus contains 82,677 documents. Reviews are embedded with `intfloat/multilingual-e5-small` (384 dimensions) and indexed with FAISS `IndexFlatIP`; vectors are normalized so inner product corresponds to cosine similarity. The answer generator is template-based and does not call an external LLM. This makes the output reproducible and keeps evidence visible.

Implementation details are documented in [`docs/retrieval_system.md`](docs/retrieval_system.md).

## Retrieval Evaluation

Manual retrieval relevance was evaluated on 15 representative queries:

| Metric | Result |
| --- | ---: |
| Precision@3 | 0.422 |
| Precision@5 | **0.507** |
| Precision@10 | 0.487 |

This is a small diagnostic benchmark, not a comprehensive production evaluation. The source table is [`results/module5/manual_precision_overall.csv`](results/module5/manual_precision_overall.csv); methodology and interpretation are in [`docs/retrieval_evaluation.md`](docs/retrieval_evaluation.md).

## Experimental Hybrid Retrieval Extension

Module 6 adds BM25 lexical retrieval, dense retrieval, Reciprocal Rank Fusion, optional reranking and transparent aspect-aware rules. It is an experimental extension rather than the core recruiter-facing contribution. Its current benchmark is a small proxy/reference experiment and must not be read as full-system accuracy or a state-of-the-art claim. Details are in [`docs/hybrid_retrieval.md`](docs/hybrid_retrieval.md).

## Analytical Web Demo

The web layer is a delivery interface for the analysis rather than the primary contribution. A FastAPI backend and HTML/CSS/JavaScript frontend provide three capabilities:

1. classify an individual review;
2. ask questions over the review corpus and inspect evidence;
3. inspect technical metrics and retrieval outputs.

See [`docs/web_demo.md`](docs/web_demo.md) for the endpoint and setup notes.

## Repository Structure

```text
data/       processed inputs, evaluation queries and aggregate reports
src/        data, sentiment, retrieval and analysis modules
models/     trained sentiment model and FAISS artifacts (Git LFS)
results/    metrics, error analysis and retrieval evaluations
figures/    selected analytical charts
backend/    FastAPI application
frontend/   browser interface
docs/       reproducibility, methodology and limitations
scripts/    runnable pipeline and demo entry points
```

## Quick Start

Large model and data artifacts use Git LFS:

```bash
git lfs install
git clone https://github.com/AlizCules/Vietnamese-Ecommerce-Sentiment-RAG.git
cd Vietnamese-Ecommerce-Sentiment-RAG
```

Install only the path being used:

```bash
python -m pip install -r requirements_module1_2.txt
python src/module2_baseline_sentiment_classification.py
```

For retrieval and the web demo:

```bash
python -m pip install -r requirements_webapp.txt
python scripts/run_rag_webapp.py
```

Open `http://127.0.0.1:8000`. Rebuilding the large FAISS index is not required for the demo when the LFS artifacts are available. The raw input files and their provenance constraints are described in [`docs/data_sources.md`](docs/data_sources.md).

## Documentation

- [`docs/data_sources.md`](docs/data_sources.md) — provenance, inputs and redistribution notes.
- [`docs/data_pipeline.md`](docs/data_pipeline.md) — cleaning, deduplication and splits.
- [`docs/review_analytics.md`](docs/review_analytics.md) — aggregate EDA and interpretation.
- [`docs/sentiment_model.md`](docs/sentiment_model.md) — model selection, metrics and errors.
- [`docs/retrieval_system.md`](docs/retrieval_system.md) — embeddings, FAISS and evidence generation.
- [`docs/retrieval_evaluation.md`](docs/retrieval_evaluation.md) — manual retrieval evaluation.
- [`docs/hybrid_retrieval.md`](docs/hybrid_retrieval.md) — Module 6 experimental extension.
- [`docs/web_demo.md`](docs/web_demo.md) — analytical web delivery layer.
- [`docs/development_notes.md`](docs/development_notes.md) — local development and validation.

## Limitations

- Sentiment labels are derived from star ratings, not independent human sentiment annotations.
- Original dataset provenance and redistribution rights are not fully verified in the tracked project material.
- Retrieval relevance was manually assessed on only 15 queries; Precision@5 is approximately 0.507.
- The Module 6 result is a small proxy/reference benchmark.
- Answer generation is template-based, not an external LLM.
- Retrieval quality depends on embedding coverage, corpus composition and metadata quality.
- This is a reproducible project prototype, not a production customer-insight platform.

## Project Context and Attribution

The tracked repository contains coursework-oriented artifacts but does not provide sufficient evidence to establish whether the work was an individual or team project, nor does it verify individual contributions. No attribution claim is made here. Historical commit metadata is preserved unchanged.

## License and Data Notice

No repository license is currently declared. Before redistributing code or row-level review artifacts, verify the original dataset license and any privacy or platform terms. The repository includes a source and redistribution note in [`docs/data_sources.md`](docs/data_sources.md).
