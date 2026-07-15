from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import numpy as np

class PredictionService:
    """Сервис батч-классификации сообщений."""

    def __init__(self, embedding_model: SentenceTransformer, classifiers: dict[str, LogisticRegression]):
        self.embedding_model = embedding_model
        self.classifiers = classifiers
        print(self.classifiers.keys())

    def predict_batch(self, texts: list[str]) -> dict[str, list] | None:
        """Размечаем всеми моделями, возвращаем метки и confidence."""
        if not texts:
            return None

        predicts: dict[str, list] = {}
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
        for name, model in self.classifiers.items():
            preds = model.predict(embeddings)
            probs = model.predict_proba(embeddings)
            predicts[name] = preds.tolist()
            predicts[f"{name}_confidence"] = [float(max(prob)) for prob in probs]

        return predicts
