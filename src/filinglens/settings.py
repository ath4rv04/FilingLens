import os
from pathlib import Path

# ---------- Project ----------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ---------- Data ----------
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FINANCE_DB_PATH = DATA_DIR / "finance.db"

# ---------- Models ----------
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5")
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "64"))

# ---------- Chunking ----------
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# ---------- Vector DB ----------
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "filinglens")
QDRANT_URL = os.getenv("QDRANT_URL", str(DATA_DIR / "qdrant"))
VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", "1024"))

# ---------- Rendering ----------
IMAGE_SCALE = int(os.getenv("IMAGE_SCALE", "2"))
SCANNED_PAGE_THRESHOLD = int(os.getenv("SCANNED_PAGE_THRESHOLD", "20"))

# ---------- LLM ----------------
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
TOP_K = int(os.getenv("TOP_K", "5"))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "6000"))
MAX_RETRIEVAL_RESULTS = int(os.getenv("MAX_RETRIEVAL_RESULTS", "5"))

# ---------- Runtime / API ----------
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "60.0"))
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "60.0"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
