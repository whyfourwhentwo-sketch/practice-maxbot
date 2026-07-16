from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Type

import redis
from pydantic import BaseModel
from redis.exceptions import ResponseError

from shared.config import INFERENCE_CONSUMER_GROUP, INFERENCE_STREAM, REDIS_URL
from shared.queue.schemas import InferenceMessage


@dataclass(frozen=True)
class StreamEntry:
    entry_id: str
    message: BaseModel


class MessageBroker:
    """Брокер на Redis Streams: publish / consumer group / batch read / ack."""

    def __init__(
        self,
        redis_url: str | None = None,
        stream: str | None = None,
        group: str | None = None,
    ) -> None:
        self._redis = redis.from_url(redis_url or REDIS_URL, decode_responses=True)
        self._stream = stream or INFERENCE_STREAM
        self._group = group or INFERENCE_CONSUMER_GROUP

    @property
    def client(self) -> redis.Redis:
        return self._redis

    def publish(self, message: BaseModel) -> str:
        payload = message.model_dump()
        if not payload.get("enqueued_at"):
            payload["enqueued_at"] = datetime.now(timezone.utc).isoformat()
        entry_id = self._redis.xadd(self._stream, {"payload": json.dumps(payload, ensure_ascii=False)})
        return entry_id

    def ensure_consumer_group(self) -> None:
        try:
            self._redis.xgroup_create(self._stream, self._group, id="0", mkstream=True)
        except ResponseError as exc:
            if "BUSYGROUP" not in str(exc):
                raise

    def read_batch(
        self,
        consumer_name: str,
        count: int = 64,
        block_ms: int = 5000,
        message_model: Type[BaseModel] = InferenceMessage,
    ) -> list[StreamEntry]:
        self.ensure_consumer_group()
        records = self._redis.xreadgroup(
            groupname=self._group,
            consumername=consumer_name,
            streams={self._stream: ">"},
            count=count,
            block=block_ms,
        )
        entries: list[StreamEntry] = []
        for _stream_name, items in records or []:
            for entry_id, fields in items:
                payload = json.loads(fields["payload"])
                entries.append(StreamEntry(entry_id=entry_id, message=message_model(**payload)))
        return entries

    def ack(self, entry_ids: list[str]) -> int:
        if not entry_ids:
            return 0
        return self._redis.xack(self._stream, self._group, *entry_ids)

    def ping(self) -> bool:
        return bool(self._redis.ping())
