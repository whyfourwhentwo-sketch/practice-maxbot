from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PredictionRecord:
    chat_id: int
    message_id: int
    label: int
    text: str


class StatsRepository:
    """Заглушка репозитория PostgreSQL. Реальная схема будет добавлена позже."""

    def __init__(self, database_url: str | None = None) -> None:
        self._database_url = database_url
        self._connected = False

    def connect(self) -> None:
        # TODO: подключить psycopg/SQLAlchemy, когда схема будет определена.
        self._connected = True

    def save_batch(self, records: list[PredictionRecord]) -> None:
        if not records:
            return
        # TODO: INSERT INTO predictions ...
        print(f"[StatsRepository stub] would save {len(records)} records to Postgres")

    def get_chat_stats(self, chat_id: int | None = None) -> dict[str, Any]:
        # TODO: SELECT aggregated stats FROM ...
        return {
            "chat_id": chat_id,
            "useful_count": 0,
            "useless_count": 0,
            "total": 0,
            "stub": True,
        }
