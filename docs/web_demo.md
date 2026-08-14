# Analytical Web Demo

The web layer exposes the project outputs through a lightweight FastAPI backend and an HTML/CSS/JavaScript frontend. It is a delivery layer for the analysis, not a replacement for the documented data and evaluation artifacts.

## Capabilities

1. Classify an individual review with the stored sentiment pipeline.
2. Ask a question over the review corpus and inspect retrieved evidence.
3. Inspect configuration, model metrics and retrieval information.

## Running locally

Install the web-app dependencies:

```bash
python -m pip install -r requirements_webapp.txt
python scripts/run_rag_webapp.py
```

Then open `http://127.0.0.1:8000`. The backend routes are implemented in `backend/app.py`; the browser assets are under `frontend/`.

The demo expects the stored sentiment model and the Module 4 FAISS/metadata artifacts. It does not download an external LLM or rebuild the 82,677-document index.
