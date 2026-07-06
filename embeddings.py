from sentence_transformers import SentenceTransformer
import numpy as np
from torch import Tensor

from config import MODEL_NAME, EMBEDDINGS_FILE


def load_embedding_model() -> SentenceTransformer:
    """Загружает модель для создания эмбеддингов."""
    return SentenceTransformer(MODEL_NAME)


def create_embeddings(phrases: list[str], model: SentenceTransformer) -> Tensor:
    """Создает эмбеддинги для списка фраз."""
    return model.encode(phrases, show_progress_bar=True)


def save_embeddings(embeddings: np.ndarray, labels: np.ndarray) -> None:
    """Сохраняет эмбеддинги и метки в файл."""
    np.savez(EMBEDDINGS_FILE, embeddings=embeddings, labels=labels)


def load_embeddings() -> tuple[np.ndarray, np.ndarray]:
    """Загружает эмбеддинги и метки из файла."""
    data = np.load(EMBEDDINGS_FILE, allow_pickle=True)
    return data['embeddings'], data['labels']