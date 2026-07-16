from shared.config import LABELS

def format_prediction(name: str, prediction: int) -> str:
    """Форматирует результат предсказания."""        
    return LABELS[name][prediction]
