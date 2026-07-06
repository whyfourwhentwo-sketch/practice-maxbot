from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression


class PredictionService:
    """Сервис для классификации сообщений."""

    def __init__(self, embedding_model: SentenceTransformer, classifier: LogisticRegression):
        self.embedding_model = embedding_model
        self.classifier = classifier

    def predict(self, text: str) -> int:
        """Классифицирует текст и возвращает предсказание."""
        embedding = self.create_embedding(text)
        return self.classify(embedding)

    def create_embedding(self, text: str):
        """Создает эмбеддинг для текста."""
        return self.embedding_model.encode([text])

    def classify(self, embedding) -> int:
        """Классифицирует эмбеддинг."""
        return self.classifier.predict(embedding)[0]