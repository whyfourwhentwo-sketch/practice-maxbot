import numpy as np
from sentence_transformers import SentenceTransformer

from shared.config import EMBEDDINGS_FILE, MODEL_NAME


def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def create_embeddings(phrases: list[str], model: SentenceTransformer) -> np.ndarray:
    return np.array(model.encode(phrases, show_progress_bar=True))


def save_embeddings(embeddings: np.ndarray, labels: np.ndarray) -> None:
    EMBEDDINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    np.savez(EMBEDDINGS_FILE, embeddings=embeddings, labels=labels)


def load_embeddings() -> tuple[np.ndarray, np.ndarray]:
    data = np.load(EMBEDDINGS_FILE, allow_pickle=True)
    return data["embeddings"], data["labels"]
