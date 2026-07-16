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

    def predict_single_model(self, embeddings, clf: LogisticRegression, relative_predicts: list[int] | None = None, filtering_label: int | None = None) -> list[int | None]:
        """
        Предикты единой моделью с фильтрацией на базе другой модели
        
        relative_predicts - массив предиктов другой модели
        filtering_label - фильтрующая метка, будут сделаны предсказания только на эмбеддинги, размеченные этой меткой ранее
        """
        
        if relative_predicts is not None and filtering_label is not None:
            result = [None] * len(embeddings)
            indices = [i for i, p in enumerate(relative_predicts) if p == filtering_label]
            if indices:
                filtered_embeddings = embeddings[indices]
                preds = clf.predict(filtered_embeddings)
                for i, pred in zip(indices, preds):
                    result[i] = pred
            return result
        return clf.predict(embeddings).tolist()
    
    
    def predict_single_proba(self, embeddings, clf: LogisticRegression, relative_predicts: list[int] | None = None, filtering_label: int | None = None) -> list[int]:
        """
        Уверенность модели с фильтрацией на базе другой модели
        
        relative_predicts - массив предиктов другой модели
        filtering_label - фильтрующая метка, будут сделаны предсказания только на эмбеддинги, размеченные этой меткой ранее
        """
        
        if relative_predicts is not None and filtering_label is not None:
            result = [None] * len(embeddings)
            indices = [i for i, p in enumerate(relative_predicts) if p == filtering_label]
            if indices:
                filtered_embeddings = embeddings[indices]
                preds = clf.predict_proba(filtered_embeddings)
                for i, pred in zip(indices, preds):
                    result[i] = pred
            return result
        return clf.predict_proba(embeddings).tolist()
    
    
    def predict_batch(self, texts: list[str]) -> dict[str, list] | None:
        """Размечаем всеми моделями, возвращаем метки и confidence."""
        if not texts:
            return None

        predicts: dict[str, list] = {}
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
        for name, model in self.classifiers.items():
            if(name in LABELS_RELATIONS):
                preds = self.predict_single_model(embeddings, model, predicts[LABELS_RELATIONS[name]["based_on"]], LABELS_RELATIONS[name]["filtering_label"])
                probs = self.predict_single_proba(embeddings, model, predicts[LABELS_RELATIONS[name]["based_on"]], LABELS_RELATIONS[name]["filtering_label"])
                
            else:
                preds = model.predict(embeddings)
                probs = model.predict_proba(embeddings)
            predicts[name] = preds.tolist()
            predicts[f"{name}_confidence"] = [float(max(prob)) for prob in probs]

        return predicts
