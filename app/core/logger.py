import logging
import os

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
    handlers=[
        logging.FileHandler(
            f"{LOG_DIR}/app.log"
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logging.getLogger(
    "huggingface_hub"
).setLevel(logging.WARNING)

logging.getLogger(
    "sentence_transformers"
).setLevel(logging.WARNING)

logging.getLogger(
    "watchfiles"
).setLevel(logging.WARNING)

logging.getLogger(
    "chromadb"
).setLevel(logging.WARNING)

logger = logging.getLogger("intellexa-ai")