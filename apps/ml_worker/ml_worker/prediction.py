from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression


class PredictionService:
    """Сервис батч-классификации сообщений."""

    def __init__(self, embedding_model: SentenceTransformer, classifier: LogisticRegression):
        self.embedding_model = embedding_model
        self.classifier = classifier

    def predict_batch(self, texts: list[str]) -> list[int]:
        if not texts:
            return []
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
        return self.classifier.predict(embeddings).tolist()
