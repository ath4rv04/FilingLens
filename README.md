# FilingLens-IN 

A highly-scalable robust semantic search tool for querying financial filings, executing Retrieval Augmented Generation (RAG) using Ollama local endpoints.

## Installation and Setup

### 1. Install Ollama and Dependencies
Ensure you have the virtual environment activated and dependencies installed:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Ensure Ollama is installed on your local machine. You can download it directly from [Ollama.com](https://ollama.com).

### 2. Pull the Base Model
FilingLens relies on Qwen2.5 (3-Billion parameters) by default. Execute the following command in your terminal while the Ollama daemon is running:
```bash
ollama pull qwen2.5:3b
```


## Workflow and Usage

### 1. Indexing a Filing
First, load the relevant financial filings (like annual reports in PDF form or raw chunks). Use the ingest script to chunk the items, generate embeddings through SentenceTransformers on Torch, and insert them into the Qdrant local Vector DB instance.

```bash
python scripts/build_index.py
```
*(Make sure Qdrant is either configured correctly locally, or your tests will run the mocks without issue)*


### 2. Ask Questions
With the index and Ollama setup active, you can submit analytical questions to the CLI directly:

```bash
python scripts/ask.py --company TCS --year FY2024 --question "What was the revenue growth in FY2024?"
```

This will autonomously execute the `QAService` pipeline.
1. The script initializes Hybrid search fetching context from **BM25** and **Dense Retrieval** algorithms via RRF scores.
2. Formats citations uniformly (e.g. `[1] TCS FY2024 Page 117`).
3. Projects instructions via `RagPromptBuilder`.
4. Streams results backward rendering latency metrics across your terminal logic automatically.

---
### Testing
You do not need an active Ollama process to run unit tests. Assertions operate off HTTP intercept mocks mapping direct namespace JSON blobs.

```bash
.venv\Scripts\pytest
```
