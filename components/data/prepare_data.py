import numpy as np
from components.data.excel_handler import load_excel_data
from components.data.embeddings_handler import create_embeddings, save_embeddings, load_embeddings, load_embedding_model

def prepare_data() -> tuple[np.ndarray, np.ndarray]:
    """Загружает эмбеддинги с метками."""
    try:
        return load_embeddings()
    except FileNotFoundError:
        """Если ничего нет, крашим нахуй, без данных не можем работать"""
        phrases, labels = load_excel_data()
        embeddings = create_embeddings(phrases)
        save_embeddings(embeddings, labels)
        return embeddings, labels
            