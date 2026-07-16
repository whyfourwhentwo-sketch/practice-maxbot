import numpy as np
from sentence_transformers import SentenceTransformer

from shared.config import EMBEDDINGS_FILE, LABELS_DIR, MODEL_NAME


def load_embedding_model() -> SentenceTransformer:
    """Загрузка языковой модели"""
    return SentenceTransformer(MODEL_NAME)


def create_embeddings(phrases: list[str], model: SentenceTransformer) -> np.ndarray:
    """Создание эмбеддингов"""
    return np.array(model.encode(phrases, show_progress_bar=True))


def save_embeddings(embeddings: np.ndarray) -> None:
    """Сохранение эмбеддингов"""
    print("Сохраняем эмбеддинги")
    EMBEDDINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    np.save(EMBEDDINGS_FILE, embeddings)


def load_embeddings() -> np.ndarray:
    """Загрузка эмбеддингов"""
    print("Грузим эмбеддинги")
    data = np.load(EMBEDDINGS_FILE)
    return data