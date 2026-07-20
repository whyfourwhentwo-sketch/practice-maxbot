from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import numpy as np

from shared.config import LABELS_RELATIONS

class PredictionService:
    """Сервис батч-классификации сообщений."""

    def __init__(self, embedding_model: SentenceTransformer, classifiers: dict[str, LogisticRegression]):
        self.embedding_model = embedding_model
        self.classifiers = classifiers
        print(self.classifiers.keys())

    def predict_single_model(self, embeddings, clf: LogisticRegression, relative_predicts: list[int] | None = None, filtering_label: int | None = None) -> tuple:
        """Предикт + уверенность с учетом возможных зависимостей у модели"""
        print('=' * 50)
        
        if(relative_predicts is not None and filtering_label is not None):
            
            indices = [i for i, value in enumerate(relative_predicts) if value == filtering_label]
            print(f"Индексы: {indices}")
            
            preds = [None] * len(embeddings)
            probs = [None] * len(embeddings)
            
            if len(indices) == 0: return preds, probs
            filtered_embeddings = np.array(embeddings)[indices]
            filtered_preds = clf.predict(filtered_embeddings)
            filtered_proba = clf.predict_proba(filtered_embeddings)
            
            for i, pred, prob in zip(indices, filtered_preds, filtered_proba):
                preds[i] = int(pred)
                probs[i] = prob
            
            return preds, probs
        return clf.predict(embeddings), clf.predict_proba(embeddings)
            
    
    
    def predict_single_proba(self, embeddings, clf: LogisticRegression, relative_predicts: list[int] | None = None, filtering_label: int | None = None) -> list[int]:
        """Deprecated: Уверенность с учетом зависимостей модели"""
        print('=' * 50)
        preds = [None] * len(embeddings)
        print(f"Макет предиктов: {preds}")
        if(relative_predicts is not None and filtering_label is not None):
            indices = [i for i, value in enumerate(relative_predicts) if value == filtering_label]
            print(f"Индексы: {indices}")
            if len(indices) == 0: return preds
            filtered_embeddings = np.array(embeddings)[indices]
            filtered_preds = clf.predict_proba(filtered_embeddings)
            
            for i, value in zip(indices, filtered_preds):
                preds[i] = value
            
            print(f"Финалочка: {preds}")
            return preds
        return clf.predict_proba(embeddings)
    
    
    def predict_batch(self, texts: list[str]) -> dict[str, list] | None:
        """Размечаем всеми моделями, возвращаем метки и confidence."""
        if not texts:
            return None

        predicts: dict[str, list] = {}
        embeddings = np.array(self.embedding_model.encode(texts, show_progress_bar=False))
        for name, model in self.classifiers.items():
            relation = LABELS_RELATIONS.get(name, {})
            relative_predicts = predicts.get(relation.get("based_on"))
            filtering_label = relation.get("filtering_label")
            
            preds, probs = self.predict_single_model(embeddings, model, relative_predicts, filtering_label)
            
            print(type(preds))
            predicts[name] = list(preds)
            print("чекпоинт")
            predicts[f"{name}_confidence"] = [None if prob is None else float(max(prob)) for prob in probs]

        return predicts
