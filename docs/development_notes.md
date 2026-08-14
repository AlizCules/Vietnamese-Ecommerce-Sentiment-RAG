# Development and Validation Notes

## Environment

The repository separates requirements for the data/sentiment path, retrieval path, Module 6 extension and web app. Versions are not guessed in this documentation; use the listed requirement files and record the local environment when reproducing results.

## Large artifacts

Git LFS stores the large processed corpora, FAISS index, metadata and model artifacts. Run `git lfs install` before cloning. Lightweight checks intentionally avoid downloading embedding models or rebuilding the index.

## Validation boundaries

Repository checks compile Python sources and validate small JSON/CSV contracts. Full sentiment training and retrieval-index construction are data- and resource-dependent workflows and are not part of CI.

## Scope discipline

Reported metrics are read from tracked result artifacts. Portfolio documentation does not alter labels, splits, model files, FAISS artifacts or manual retrieval annotations.
