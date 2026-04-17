import json
import logging
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "rag_app.log"

logger = logging.getLogger("rag_app")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(file_handler)


def log_query(request_id: str, query: str, source_count: int, sources: list[str], status: str = "success"):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "request_id": request_id,
        "query": query,
        "source_count": source_count,
        "sources": sources,
        "status": status,
    }
    logger.info(json.dumps(log_entry))