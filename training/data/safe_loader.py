import numpy as np

from training.data.embeddings_handler import load_embeddings, create_embeddings, load_embedding_model, save_embeddings
from training.data.excel_handler import new__get_excel


def create_data():
    """Создание данных, если их нет"""
    # Я пока не могу придумать норм архитектуру, пока пусть грузит фулл данные всегда
    # В планах подгрузка только того, чего нет для оптимизации памяти + аргументы для перезаписи существующих моделей
    # Ну сначала надо под такую архитектуру переписать загрузку/сохранение данных, WIP методы для эксельки валяются. Они рабочие, просто как их подтянуть, я пока не додумался
    None


def load_data_safe(file_path) -> tuple[np. ndarray, np.ndarray, dict[str, np.ndarray]]:
    """Грузим данные (WIP)"""

    parsed = new__get_excel(file_path)  # Если нет эксель данных, дальше двигаться смысла нет

    try:
        embeddings = load_embeddings()
    except (FileNotFoundError):
        embeddings = create_embeddings(parsed["text"], load_embedding_model())
        save_embeddings(embeddings)
    return parsed["text"], embeddings, {key: value for key, value in parsed.items() if key != "text"}
