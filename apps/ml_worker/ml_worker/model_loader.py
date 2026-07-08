import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

from shared.config import MODEL_FILE, MODEL_NAME


def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def load_classifier() -> LogisticRegression:
    return joblib.load(MODEL_FILE)
