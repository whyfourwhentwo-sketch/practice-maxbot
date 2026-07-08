def format_prediction(prediction: int) -> str:
    """Форматирует результат предсказания."""
    return "Полезное" if prediction == 1 else "Бесполезное"
