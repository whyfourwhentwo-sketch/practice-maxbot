from flask import Flask, jsonify, request

from .cache import StatsCache
from shared.config import API_HOST, API_PORT
from shared.db import StatsRepository
from shared.queue import MessageBroker

# WebSocket (flask-socketio) будет добавлен, когда появится фронтенд.
# Бэкенд сможет пушить события stats:updated при записи в Postgres.


def create_app() -> Flask:
    app = Flask(__name__)
    stats_repo = StatsRepository()
    stats_repo.connect()
    cache = StatsCache()
    broker = MessageBroker()

    @app.get("/health")
    def health():
        return jsonify({
            "status": "ok",
            "redis": broker.ping(),
            "cache": cache.ping(),
            "postgres": "stub",
        })

    @app.get("/stats")
    def stats():
        chat_id = request.args.get("chat_id", type=int)
        cache_key = f"stats:{chat_id or 'all'}"

        cached = cache.get_stats(cache_key)
        if cached is not None:
            return jsonify({**cached, "cached": True})

        payload = stats_repo.get_chat_stats(chat_id)
        cache.set_stats(cache_key, payload)
        return jsonify({**payload, "cached": False})

    @app.get("/")
    def home():
        return jsonify({
            "service": "practice-maxbot-api",
            "endpoints": ["/health", "/stats?chat_id=<id>"],
        })

    return app


def main() -> None:
    app = create_app()
    app.run(host=API_HOST, port=API_PORT)


if __name__ == "__main__":
    main()
