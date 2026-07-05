from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Пути к файлам
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data_ml.xlsx"
EMBEDDINGS_FILE = BASE_DIR / "data.npz"
MODEL_FILE = BASE_DIR / "model.pkl"

# Telegram
BOT_TOKEN = os.getenv("TOKEN")

# ML
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
TEST_SIZE = 0.2
RANDOM_STATE = 42
MAX_ITER = 1000

# Excel
EXCEL_RANGE = "A1:D311"
PHRASE_COLUMN = 0
LABEL_COLUMN = 3
LABEL_POSITIVE = "да"