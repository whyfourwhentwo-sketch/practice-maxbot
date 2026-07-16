import json

import redis

from shared.config import CACHE_TTL_SECONDS, REDIS_URL


class StatsCache:
    """Redis-кэш для статистики. Пока работает поверх заглушек."""

    def __init__(self, redis_url: str | None = None, ttl_seconds: int | None = None) -> None:
        self._redis = redis.from_url(redis_url or REDIS_URL, decode_responses=True)
        self._ttl = ttl_seconds or CACHE_TTL_SECONDS

    def get_stats(self, cache_key: str) -> dict | None:
        raw = self._redis.get(cache_key)
        if raw is None:
            return None
        return json.loads(raw)

    def set_stats(self, cache_key: str, payload: dict) -> None:
        self._redis.setex(cache_key, self._ttl, json.dumps(payload, ensure_ascii=False))

    def ping(self) -> bool:
        return bool(self._redis.ping())
