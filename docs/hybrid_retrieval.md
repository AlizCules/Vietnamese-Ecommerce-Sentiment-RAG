# Experimental Hybrid Retrieval Extension

Module 6 extends the dense retrieval layer with BM25 lexical search, dense FAISS retrieval, Reciprocal Rank Fusion (RRF), optional reranking and rule-based aspect analysis. It is an experimental diagnostic extension, not the primary project contribution.

## Components

- BM25 preserves exact complaint phrases such as `sai size`, `móp hộp` and `shop không trả lời`.
- Dense FAISS retrieval supplies semantic neighbors from the existing Module 4 index.
- RRF combines rankings without rebuilding the index.
- An optional CrossEncoder reranker can be used when its dependency and model cache are available; otherwise the code falls back to lexical scoring.
- Rule-based aspect sentiment produces transparent evidence tags for delivery, packaging, price, quality, shop service and size/color.

## Proxy benchmark

The tracked Module 6 benchmark is small and handcrafted. It compares BM25, dense, hybrid and hybrid-plus-reranker modes using keyword/aspect hit-rate proxies. The current reference table reports 0.500/0.667/1.000/1.000 for BM25 and 0.500/0.833/1.000/1.000 for dense across the recorded metrics, with hybrid modes scoring 1.000 on those proxy columns. These values are not full-system accuracy and should not be generalized beyond the small reference queries.

## Limitations

Keyword hit-rate is only a relevance proxy; aspect hit-rate can be high even when polarity is wrong. The module does not implement a supervised relevance model or full LLM generation. A larger manually labeled query–document benchmark is required before selecting a production retrieval strategy.

The implementation details remain in `src/module6_*.py` and `scripts/evaluate_module6_retrieval.py`.
