import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from shared.config import MAX_ITER, MODELS_DIR, RANDOM_STATE, TEST_SIZE


def train_classifier(embeddings: np.ndarray, labels: np.ndarray) -> LogisticRegression:
    
    X_train, X_test, y_train, y_test = train_test_split(
        embeddings,
        labels,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )
    classifier = LogisticRegression(class_weight="balanced", max_iter=MAX_ITER)
    classifier.fit(X_train, y_train)
    evaluate_model(classifier, X_test, y_test)
    return classifier


def evaluate_model(classifier: LogisticRegression, X_test: np.ndarray, y_test: np.ndarray) -> None:
    predictions = classifier.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(f"Classification Report:\n{classification_report(y_test, predictions)}")


def save_model(name: str, classifier: LogisticRegression) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(classifier, MODELS_DIR / f"{name}.pkl")
