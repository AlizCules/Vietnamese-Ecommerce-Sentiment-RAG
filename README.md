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

## Key Findings

- The 5,162-review base contains substantial positive and negative feedback: 42.95% positive, 40.18% negative and 16.87% neutral. These classes are derived from star ratings rather than independent human sentiment annotation.
- Neutral reviews are the hardest class to classify: the Linear SVM neutral-class F1 is approximately 0.823, consistent with short or ambiguous text that does not state a clear opinion.
- The selected classifier reaches 0.910 Macro-F1 and 0.933 accuracy, showing potential to support first-pass triage of large volumes of rating-derived customer feedback while ambiguous cases still require further review.
- The retrieval layer supports evidence-backed questions about delivery, packaging, product quality and related customer-service issues, so an analyst can inspect the underlying review snippets for product or customer-feedback analysis.
- Across 15 representative evaluation queries, Precision@5 is 0.507. This is a small manual diagnostic benchmark for retrieval relevance, not a production-quality or overall-system accuracy claim.

### Worked retrieval example

The stored Module 4 output in [`results/module4/rag_outputs.json`](results/module4/rag_outputs.json) records the following query, retrieved evidence and generated response. Nothing in this example was invented.

**Query:** `Khách hàng phàn nàn gì về giao sai hàng, giao chậm hoặc đóng gói bị móp?`

**Top retrieved evidence snippets:**

- **[1]** “Lần đầu mua hàng tại shop mình đã có trải nghiệm thật sự rất khó chịu. Giao hàng rất nhanh tuy nhiên lần đầu mình mua trắng nhưng shop giao màu đen...” (`sentiment=negative`, `category=Fashion`, `rating=1`)
- **[2]** “Shop giao sai hàng nhắn tin rất nhiều lần không trả lời , điện thoại 10 c không nghe máy...” (`sentiment=negative`, `category=Electronic`, `rating=3`)

**Generated answer:**

> Dựa trên 8 review được truy hồi, có 5 bằng chứng tiêu cực rõ ràng. Các phàn nàn chính liên quan đến: dịch vụ/shop (20), mẫu mã/size/màu (13), giá (5), giao hàng (3). Bằng chứng chính nằm ở các review [1] [2] [3]. Các phản hồi tiêu cực được ưu tiên trích dẫn khi sentiment là negative và rating thấp hoặc có dấu hiệu khiếu nại trong nội dung.

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

The descriptive layer profiles the customer-feedback base before classification and retrieval. It summarizes sentiment composition, review length, the five-level rating composition used to derive the labels, and the category mix of the retrieval corpus.

### Sentiment composition

**What was analyzed:** the distribution of the three rating-derived sentiment classes across the 5,162 deduplicated sentiment reviews.

**What was observed:** 2,217 reviews are positive (42.95%), 2,074 are negative (40.18%) and 871 are neutral (16.87%), showing substantial positive and negative feedback rather than a single dominant class.

**Why it is useful:** this provides a baseline view of the feedback mix for downstream customer-feedback analysis. It is descriptive only; the labels are not independent human annotations.

![Three-class sentiment distribution](figures/module3/sentiment_3class_distribution.png)

The aggregate source table is [`results/module3/overall_sentiment_distribution.csv`](results/module3/overall_sentiment_distribution.csv).

### Rating composition and label mapping

**What was analyzed:** the distribution of the five source rating levels and their mapping to the three sentiment classes.

**What was observed:** the rating-to-sentiment mapping is explicit in the crosstab: ratings 1–2 are negative, rating 3 is neutral, and ratings 4–5 are positive.

**Why it is useful:** this makes the label definition auditable and clarifies why sentiment composition should not be treated as independently validated sentiment measurement.

![Rating distribution](figures/module3/rag_rating_distribution.png)

The mapping source is [`results/module3/rating_sentiment_crosstab.csv`](results/module3/rating_sentiment_crosstab.csv), with the full label caveat in [`docs/review_analytics.md`](docs/review_analytics.md).

### Review length

**What was analyzed:** the text-length distribution for sentiment reviews and the retrieval corpus.

**What was observed:** the average sentiment-review length is approximately 13.13 units, while the retrieval corpus average is approximately 26.79 units. Short or ambiguous reviews are visible among difficult classification cases.

**Why it is useful:** text length provides context when interpreting both classification uncertainty and the amount of detail available for evidence retrieval.

![Review text length distribution](figures/module3/sentiment_text_length_distribution.png)

The length summaries are reported in [`results/module3/rag_sentiment_summary.json`](results/module3/rag_sentiment_summary.json).

### Retrieval corpus categories

**What was analyzed:** the category composition of the 82,677-document retrieval corpus.

**What was observed:** Fashion and Electronic are the largest represented categories, with 24,989 and 19,645 documents respectively; smaller categories have less retrieval coverage.

**Why it is useful:** corpus composition helps an analyst interpret which product areas are more strongly represented when reviewing retrieved evidence.

![Retrieval corpus category distribution](figures/module3/rag_category_distribution.png)

The category counts and corpus summary are available in [`results/module3/rag_sentiment_summary.json`](results/module3/rag_sentiment_summary.json). Further analytical notes are in [`docs/review_analytics.md`](docs/review_analytics.md).

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

The retrieval layer supports evidence-backed questions about issues such as delivery, packaging and product quality while keeping the supporting review text visible for inspection. The answer generator is template-based and does not call an external LLM. Embedding, FAISS and evidence-generation implementation details are documented in [`docs/retrieval_system.md`](docs/retrieval_system.md); the experimental Module 6 extension is documented in [`docs/hybrid_retrieval.md`](docs/hybrid_retrieval.md).

## Retrieval Evaluation

Manual retrieval relevance was evaluated on 15 representative queries:

| Metric | Result |
| --- | ---: |
| Precision@3 | 0.422 |
| Precision@5 | **0.507** |
| Precision@10 | 0.487 |

This is a small diagnostic benchmark, not a comprehensive production evaluation. The source table is [`results/module5/manual_precision_overall.csv`](results/module5/manual_precision_overall.csv); methodology and interpretation are in [`docs/retrieval_evaluation.md`](docs/retrieval_evaluation.md).

## Experimental Hybrid Retrieval Extension

Module 6 is an experimental extension rather than the core recruiter-facing contribution. Its BM25, Reciprocal Rank Fusion, reranking and aspect-analysis details are in [`docs/hybrid_retrieval.md`](docs/hybrid_retrieval.md); its small proxy/reference benchmark must not be read as full-system accuracy or a state-of-the-art claim.

## Analytical Web Demo

The web layer is a delivery interface for the analysis rather than the primary contribution. A FastAPI backend and HTML/CSS/JavaScript frontend provide four capabilities:

1. classify an individual review;
2. ask questions over the review corpus;
3. inspect the supporting evidence behind retrieved answers;
4. inspect analytical metrics and retrieval outputs.

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
