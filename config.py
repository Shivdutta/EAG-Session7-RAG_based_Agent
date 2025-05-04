import os
from pathlib import Path
import dotenv

dotenv.load_dotenv()
USE_OPENAI = True
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text:latest"

ROOT = Path(__file__).parent.resolve()
INDEX_CACHE = ROOT / "faiss_index"
INDEX_CACHE.mkdir(exist_ok=True)
INDEX_FILE = INDEX_CACHE / "index.bin"
METADATA_FILE = INDEX_CACHE / "metadata.json"
CACHE_FILE = INDEX_CACHE / "doc_index_cache.json"
CHUNK_SIZE = 256 
CHUNK_OVERLAP = 48