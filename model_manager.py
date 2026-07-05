from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import numpy as np

from config import TEST_SIZE, RANDOM_STATE, MAX_ITER, MODEL_FILE
from data_loader import load_excel_data
from embeddings import create_embeddings, save_embeddings, load_embeddings, load_embedding_model


def prepare_data() -> tuple[np.ndarray, np.ndarray]:
    """Загружает или создает эмбеддинги и метки."""
    try:
        return load_embeddings()
    except FileNotFoundError:
        return create_and_save_embeddings()


def create_and_save_embeddings() -> tuple[np.ndarray, np.ndarray]:
    """Создает эмбеддинги из Excel и сохраняет их."""
    model = load_embedding_model()
    phrases, labels = load_excel_data()
    embeddings = create_embeddings(phrases, model)
    save_embeddings(embeddings, np.array(labels))
    return embeddings, np.array(labels)


def train_classifier(embeddings: np.ndarray, labels: np.ndarray) -> LogisticRegression:
    """Обучает классификатор на эмбеддингах."""
    X_train, X_test, y_train, y_test = split_data(embeddings, labels)
    classifier = create_classifier()
    classifier.fit(X_train, y_train)
    evaluate_model(classifier, X_test, y_test)
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


def evaluate_model(classifier: LogisticRegression, X_test: np.ndarray, y_test: np.ndarray) -> None:
    """Оценивает качество модели."""
    predictions = classifier.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(f"Classification Report:\n{classification_report(y_test, predictions)}")


def load_or_train_model() -> LogisticRegression:
    """Загружает сохраненную модель или обучает новую."""
    try:
        return joblib.load(MODEL_FILE)
    except FileNotFoundError:
        return train_and_save_model()


def train_and_save_model() -> LogisticRegression:
    """Обучает модель и сохраняет её в файл."""
    embeddings, labels = prepare_data()
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Labels shape: {labels.shape}")

    model = train_classifier(embeddings, labels)
    joblib.dump(model, MODEL_FILE)
    return model