from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import numpy as np

class PredictionService:
    """Сервис батч-классификации сообщений."""

    def __init__(self, embedding_model: SentenceTransformer, classifiers: dict[str, LogisticRegression]):
        self.embedding_model = embedding_model
        self.classifiers = classifiers

    def predict_batch(self, texts: list[str]) -> dict[str, list[int]] | None:
        """Размечаем всеми моделями"""
        if not texts:
            return None
        
        predicts = {name: [] for name in self.classifiers.keys()}
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
        for name, model in self.classifiers.items():
            predicts[name] = np.array(model.predict(embeddings))
        
        return predicts
