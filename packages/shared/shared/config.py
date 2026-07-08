from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()


def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists() and (parent / "apps").exists():
            return parent
    return current.parents[3]


PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", find_project_root()))
DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))

DATA_FILE = DATA_DIR / "excel" / "data_ml.xlsx"
EMBEDDINGS_FILE = DATA_DIR / "machine" / "data.npz"
MODEL_FILE = DATA_DIR / "models" / "classifier.pkl"

BOT_TOKEN = os.getenv("TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://maxbot:maxbot@localhost:5432/maxbot",
)

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
ML_BATCH_SIZE = int(os.getenv("ML_BATCH_SIZE", "64"))
TEST_SIZE = 0.2
RANDOM_STATE = 42
MAX_ITER = 1000

EXCEL_RANGE = "A1:D311"
PHRASE_COLUMN = 0
LABEL_COLUMN = 3
LABEL_POSITIVE = "да"

INFERENCE_STREAM = os.getenv("INFERENCE_STREAM", "inference:messages")
INFERENCE_CONSUMER_GROUP = os.getenv("INFERENCE_CONSUMER_GROUP", "ml-workers")
INFERENCE_RESULT_STREAM = os.getenv("INFERENCE_RESULT_STREAM", "inference:results")
INFERENCE_RESULT_CONSUMER_GROUP = os.getenv("INFERENCE_RESULT_CONSUMER_GROUP", "bot-senders")

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))
