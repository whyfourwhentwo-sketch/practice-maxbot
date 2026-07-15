from typing import List, Any

from pydantic import BaseModel, Field, field_serializer
import numpy as np


class InferenceMessage(BaseModel):
    """Сообщение из Telegram-бота для ML-воркера."""

    message_id: int
    chat_id: int
    text: str
    user_name: str = ""
    platform: str = "tg"
    platform_user_id: int | None = None
    chat_name: str = ""
    enqueued_at: str = Field(default="", description="ISO timestamp")


class InferenceResultMessage(BaseModel):
    """Результат инференса для отправки ответа в Telegram ботом."""

    message_id: int
    chat_id: int
    prediction: int
    response_text: str
    processed_at: str = Field(default="", description="ISO timestamp")


class InferenceResultMessageTest(BaseModel):
    """Тест новой модели отправки сообщений"""
    message_id: int
    chat_id: int


class InferenceResultBatch(BaseModel):
    """Отправка сообщений батчем боту, чисто для тестов"""
    messages: list[InferenceResultMessageTest]
    predictions: dict[str, list[Any]]

    # @field_serializer('predictions')
    # def serialize_numpy_types(self, value: List[Any]) -> List[Any]:
    #     """Рекурсивно очищает структуру от типов numpy перед JSON-сериализацией"""

    #     def clean_numpy(obj):
    #         if isinstance(obj, np.ndarray):
    #             return obj.tolist()
    #         # Превращает np.int64, np.float32 и т.д. в обычные int/float
    #         elif isinstance(obj, (np.integer, np.floating, np.bool_)):
    #             return obj.item()
    #         elif isinstance(obj, list):
    #             return [clean_numpy(item) for item in obj]
    #         elif isinstance(obj, dict):
    #             return {k: clean_numpy(v) for k, v in obj.items()}
    #         return obj

    #     return clean_numpy(value)
    
class APIResponse(BaseModel):
    text: str