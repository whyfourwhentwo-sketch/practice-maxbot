from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import numpy as np

from config import TEST_SIZE, RANDOM_STATE, MAX_ITER, MODEL_FILE


def train_classifier(embeddings: np.ndarray, labels: np.ndarray) -> LogisticRegression:
    """Обучает классификатор на эмбеддингах."""
    X_train, X_test, y_train, y_test = split_data(embeddings, labels)
    classifier = create_classifier()
    classifier.fit(X_train, y_train)
    evaluate_model(classifier, X_test, y_test)
    save_model(classifier)
    return classifier


def split_data(embeddings: np.ndarray, labels: np.ndarray):
    """Разделяет данные на тренировочную и тестовую выборки."""
    return train_test_split(
        embeddings, labels,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )
    
    
def create_classifier() -> LogisticRegression:
    """Создает модель логистической регрессии."""
    return LogisticRegression(class_weight='balanced', max_iter=MAX_ITER)


def save_model(classifier: LogisticRegression) -> None:
    """Сохраняет обученную модель в файл."""
    joblib.dump(classifier, MODEL_FILE)
    
    
def evaluate_model(classifier: LogisticRegression, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Оценивает качество модели."""
    predictions = classifier.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(f"Classification Report:\n{classification_report(y_test, predictions)}")
