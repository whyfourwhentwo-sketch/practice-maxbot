from pydantic import BaseModel, Field


class InferenceMessage(BaseModel):
    """Сообщение из Telegram-бота для ML-воркера."""

    message_id: int
    chat_id: int
    text: str
    user_name: str = ""
    enqueued_at: str = Field(default="", description="ISO timestamp")


class InferenceResultMessage(BaseModel):
    """Результат инференса для отправки ответа в Telegram ботом."""

    message_id: int
    chat_id: int
    prediction: int
    response_text: str
    processed_at: str = Field(default="", description="ISO timestamp")
