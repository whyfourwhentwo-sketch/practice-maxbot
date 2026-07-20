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


"""Директории"""
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", find_project_root()))
DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))
LABELS_DIR = DATA_DIR / "machine" / "labels"
DATA_RAW_FILE = DATA_DIR / "excel" / "data_ml.xlsx"
DATA_PARSED_FILE = DATA_DIR / "parsed" / "data.npz"
EMBEDDINGS_FILE = DATA_DIR / "machine" / "embeddings.npy"
MODELS_DIR = DATA_DIR / "models"

"""Бот"""
BOT_TOKEN = os.getenv("TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")


"""API"""
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))




"""Excel парсинг (планируется убрать или урезать, т.к. будет автоподбор) (Готово, требуются тесты)"""
# EXCEL_RANGE = "A1:D311"
# PHRASE_COLUMN = 0
# LABEL_COLUMN = 3
LABELS = { # модели создаются на базе этого параметра
    "useful": ["да", "нет"],
    "sentiment": ["positive", "negative", "neutral"],
    "category": ["окна", "парковка", "пожарная сигнализация", "лифт", "кондиционер", "ук", "улица", "соседи", "животные", "вода/отопление", "потеря", "мусор", "посторонние", "запах", "электричество", "водители", "охрана", "канализация"], #WIP
}
LABELS_RELATIONS = { # связи между моделями (WIP)
    "category": {"based_on": "useful", "filtering_label": 0}
}


"""Для моделей"""
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2" # Модель для эмбеддингов
ML_BATCH_SIZE = int(os.getenv("ML_BATCH_SIZE", "64"))
TEST_SIZE = 0.2
RANDOM_STATE = 42
MAX_ITER = 1000


"""База данных"""
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://maxbot:maxbot@localhost:5435/maxbot",
)


"""Redis"""
INFERENCE_STREAM = os.getenv("INFERENCE_STREAM", "inference:messages")
INFERENCE_CONSUMER_GROUP = os.getenv("INFERENCE_CONSUMER_GROUP", "ml-workers")
INFERENCE_RESULT_STREAM = os.getenv("INFERENCE_RESULT_STREAM", "inference:results")
INFERENCE_RESULT_CONSUMER_GROUP = os.getenv("INFERENCE_RESULT_CONSUMER_GROUP", "bot-senders")



