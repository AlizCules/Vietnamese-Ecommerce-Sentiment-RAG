# Data Sources and Provenance

## Verified source information

The tracked project material identifies two project-provided Vietnamese e-commerce review inputs:

- `Data_sent.xlsx` for the supervised sentiment workflow;
- `RAG.zip` for the retrieval corpus.

The original public URL, publisher, license and collection procedure are not established by the tracked repository. No marketplace, benchmark or third-party dataset name is inferred without supporting evidence. Before broader redistribution or reuse, the original source and its terms should be verified.

## Dataset scale

- Sentiment input: 5,971 raw rows; 5,162 rows after deduplication; 46 conflicting duplicate rows removed.
- Retrieval corpus: 82,677 final documents.
- Final retrieval artifacts: `models/module4/review_metadata.parquet` and `models/module4/review_faiss.index`.

## Processing and derived artifacts

The data layer normalizes text, removes duplicate or conflicting records, and creates stratified sentiment splits. The retrieval layer removes empty and duplicate documents according to the recorded pipeline summary, then stores document metadata and dense vectors. Aggregate summaries are kept under `data/reports/` and `results/`.

## Redistribution note

Some processed CSV/JSONL files contain row-level review text and are tracked with Git LFS. Their presence in this repository is not evidence that the underlying review data is freely redistributable. Users should verify licensing, privacy and platform terms before publishing mirrors or building public services from the artifacts.

## Reproducibility note

The repository preserves the processed artifacts used for the reported metrics. Recreating them from raw inputs requires obtaining the original project-provided files and confirming that their use is permitted. The exact counts and paths are recorded in `data/reports/data_summary.json`.
