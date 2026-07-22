import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

from shared.config import MODELS_DIR, MODEL_NAME, LABELS, CONFIG_FILE


def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def load_classifiers() -> dict[str, LogisticRegression]:
    """Загрузка моделей."""
    classifiers = {}

    for name in LABELS.keys():
        model_path = MODELS_DIR / f"{name}.pkl"

        if not model_path.exists():
            raise FileNotFoundError(
                f"ERROR: Отсутствует обязательная модель '{name}'.\n"
                f"Ожидаемый путь: {model_path.resolve()}\n"
                f"Проверьте, что файлы моделей корректно скопированы в директорию {MODELS_DIR.resolve()}\n"
                f"Если данная модель была необязательна, исключите ее из файла конфигурации {CONFIG_FILE.resolve()}"
            )

        try:
            classifiers[name] = joblib.load(model_path)
        except Exception as e:
            raise RuntimeError(
                f"ERROR: Не удалось прочитать модель '{name}'.\n"
                f"Путь: {model_path.resolve()}\n"
                f"Причина: {e}"
            )

    return classifiers
        
