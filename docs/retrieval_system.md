# Evidence Retrieval and Answer Generation

## Core pipeline

The retrieval layer follows:

`Query → query expansion → dense retrieval → optional metadata filtering → evidence selection → template-based answer`

The final corpus contains 82,677 documents. The embedding model is `intfloat/multilingual-e5-small`, producing 384-dimensional vectors. FAISS `IndexFlatIP` is used with normalized vectors, so inner product is equivalent to cosine similarity.

The main artifacts are:

- `models/module4/review_faiss.index`;
- `models/module4/review_metadata.parquet`;
- `models/module4/module4_index_config.json`.

## Evidence-grounded output

The answer generator selects review evidence and produces a deterministic template-based response. It does not call an external LLM or claim generative model quality. The design keeps retrieved text, metadata and filtering decisions inspectable.

## Rebuild boundary

The web demo loads the existing index and metadata. Rebuilding the index requires the source corpus, the embedding dependencies and substantial local resources; it is intentionally outside lightweight CI.
