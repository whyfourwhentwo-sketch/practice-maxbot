
import joblib
from sklearn.linear_model import LogisticRegression

from config import MODEL_FILE
from components.data.prepare_data import prepare_data
from components.model.model_train import train_classifier


def get_classifier() -> LogisticRegression:
    """Загружает классификатор из файла или создает новый."""
    try:
        return joblib.load(MODEL_FILE)
    except FileNotFoundError:
        embeddings, labels = prepare_data()
        return train_classifier(embeddings, labels)