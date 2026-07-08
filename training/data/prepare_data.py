import numpy as np

from training.data.excel_handler import load_excel_data
from training.data.embeddings_handler import (
    create_embeddings,
    load_embedding_model,
    load_embeddings,
    save_embeddings,
)


def prepare_data() -> tuple[np.ndarray, np.ndarray]:
    """Загружает эмбеддинги с метками или генерирует из Excel."""
    try:
        return load_embeddings()
    except FileNotFoundError:
        phrases, labels = load_excel_data()
        model = load_embedding_model()
        embeddings = create_embeddings(phrases, model)
        save_embeddings(embeddings, labels)
        return embeddings, labels
