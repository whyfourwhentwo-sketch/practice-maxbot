import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

from shared.config import MODELS_DIR, MODEL_NAME, LABELS


def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def load_classifiers() -> dict[str, LogisticRegression]:
    """Загрузка моделек"""
    # При отсутствии модельки лучше крашить от греха подальше
    # Возможно стоит подгружать из директории, но тогда, если какой-то модели нет - мы этого не узнаем, а в конфиге модели не просто так прописаны - они должны быть по идее
    return {name: joblib.load(MODELS_DIR / f"{name}.pkl") for name, label in LABELS.items()}
        
