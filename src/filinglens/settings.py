from pathlib import Path

# ---------- Project ----------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ---------- Data ----------

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

# ---------- Models ----------

EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"

EMBEDDING_BATCH_SIZE = 64

# ---------- Chunking ----------

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# ---------- Vector DB ----------

QDRANT_COLLECTION = "filings"

QDRANT_URL = "http://localhost:6333"

VECTOR_DIMENSION = 1024

# ---------- Rendering ----------

IMAGE_SCALE = 2

# ---------- Text Extraction ----------

SCANNED_PAGE_THRESHOLD = 20

# --------------------------------------------------
# LLM
# --------------------------------------------------

LLM_PROVIDER = "ollama"

OLLAMA_MODEL = "qwen2.5:3b"

OLLAMA_HOST = "http://localhost:11434"