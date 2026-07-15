from openpyxl import load_workbook
import numpy as np

from shared.config import DATA_FILE, LABELS, LABELS_DIR


def load_excel_data(path=None) -> tuple[list[str], dict[str, np.ndarray]]:
    """Подгружаем таблицу, парсим"""
    print(f"Грузим эксель таблицу из {path or DATA_FILE}")
    workbook = load_workbook(path or DATA_FILE)
    sheet = workbook.active
    return parse_excel_rows(sheet)


def get_headers(sheet) -> list[str]:
    """Получаем заголовки столбцов"""
    print("Получаем заголовки")
    return [str(cell).strip() for cell in next(sheet.iter_rows(min_row=1, max_row=1, min_col=2, max_col=sheet.max_column, values_only=True))]


def parse_excel_rows(sheet) -> tuple[list[str], dict[str, np.ndarray]]:
    """Парсим строки"""
    print("Парсим данные")
    headers = get_headers(sheet) # Заголовки
    
    # Словарик полезных заголовков и индексов, полезные заголовки - которые есть и в файле и в конфиге
    header_indices = {header: i + 1 for i, header in enumerate(headers) if header in LABELS} 
    print(f"Столбцы к обработке: {header_indices.keys()}")
    
    # словарик меток
    phrases = []
    labels = {f"{header}": [] for header in header_indices.keys()}

    # Парсим полезные столбцы
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=sheet.max_column, values_only=True):
        phrases.append(str(row[0]).strip())
        for header, i in header_indices.items():
            #print(f"Смотрим столбец {header}, индекс {i}")
            labels[header].append(convert_label(header, str(row[i]).strip()))
            
    labels_numpy = {header: np.array(label) for header, label in labels.items()}
    return phrases, labels_numpy

    
def convert_label(name: str, value: str) -> int:
    """Конвертация с настройкой в конфиге, чтобы сюда не лезть"""
    return LABELS[name].index(value)
    





"""Архитектура не до конца ясна для методов ниже, пока не используются"""

def save_labels(name: str, labels: list[str]) -> None:
    """Сохранение меток в разные файлы по имени (WIP)"""
    LABELS_DIR.mkdir(parents=True, exist_ok=True)
    np.save(LABELS_DIR / f"{name}.npy", np.array(labels))
    
    
def load_labels(name: str) -> np.ndarray:
    """Загрузка меток по имени (WIP)"""
    data = np.load(LABELS_DIR / f"{name}.npy")
    return data
    