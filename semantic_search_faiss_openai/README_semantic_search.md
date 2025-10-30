
# Semantic Search Engine — OpenAI + FAISS

**Files in this package**
- `semantic_search_faiss_openai.ipynb`: main notebook with end-to-end implementation.
- `sample_corpus.zip`: 240+ plain-text documents grouped by category.
- `requirements.txt`: minimal package list.

## Quickstart (Local Python)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U -r requirements.txt
export OPENAI_API_KEY="sk-..."                      # Windows PowerShell: $Env:OPENAI_API_KEY="sk-..."
```

Open the notebook and run through sections 1 → 7.

## Quickstart (Google Colab)

- Upload `semantic_search_faiss_openai.ipynb` and `sample_corpus.zip`.
- In the first code cell, optionally run the `pip install` line.
- Unzip the sample corpus next to the notebook (if needed).
- Set your `OPENAI_API_KEY` in the Colab environment (`Settings → Secrets` or `%env`).
- Run sections 1 → 7.

## Notes

- The notebook automatically **falls back** to a local hashing embedding and a NumPy index if OpenAI/FAISS are unavailable.
- For your assignment submission, ensure you run the **OpenAI + FAISS** path and include the demo outputs.
