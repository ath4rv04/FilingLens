# FilingLens-IN

Multimodal multi-agent financial filing intelligence for Indian markets.

## Current Build Slice

The project currently supports:

- PDF page rendering and text extraction
- Page-level chunking into `DocumentChunk` JSON files
- SentenceTransformer embeddings
- Dense vector indexing and search with Qdrant

## Local Setup

Install the package in editable mode:

```powershell
pip install -e .
```

Start Qdrant:

```powershell
docker compose up -d qdrant
```

Process a filing PDF:

```powershell
python scripts/process_document.py --input data/raw/TCS/FY2024/annual_report.pdf
```

Build the dense vector index:

```powershell
python scripts/build_index.py --chunks data/processed/TCS/FY2024/chunks --recreate
```

Search indexed chunks:

```powershell
python scripts/search.py --question "What drove revenue growth?" --top-k 5
```

Run hybrid dense + BM25 search:

```powershell
python scripts/hybrid_search.py --question "What drove revenue growth?" --chunks data/processed/TCS/FY2024/chunks --top-k 5
```

Extract tables into CSV files:

```powershell
python scripts/extract_tables.py --input data/raw/TCS/FY2024/annual_report.pdf --output data/processed/TCS/FY2024/tables
```

Ask simple questions over extracted table CSVs:

```powershell
python scripts/table_qa.py --tables data/processed/TCS/FY2024/tables --question "FY2024 revenue"
```

Assemble cited context for a future RAG answer:

```powershell
python scripts/assemble_context.py --question "What drove revenue growth?" --chunks data/processed/TCS/FY2024/chunks --top-k 5
```

Run OCR over rendered pages:

```powershell
python scripts/ocr_pages.py --pages data/processed/TCS/FY2024/pages --output data/processed/TCS/FY2024/ocr
```

Run visual page retrieval:

```powershell
python scripts/visual_search.py --pages data/processed/TCS/FY2024/pages --question "revenue chart" --top-k 5
```

Start the API:

```powershell
uvicorn filinglens.api:app --reload
```

Run checks:

```powershell
ruff format .
ruff check .
pytest
```
