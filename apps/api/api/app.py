from flask import Flask, jsonify, request
from flask_cors import CORS

from .cache import StatsCache
from shared.config import API_HOST, API_PORT, INFERENCE_RESULT_STREAM, INFERENCE_RESULT_CONSUMER_GROUP
from shared.db import StatsRepository
from shared.queue import MessageBroker


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    stats_repo = StatsRepository()
    stats_repo.connect()
    cache = StatsCache()
    broker = MessageBroker(stream=INFERENCE_RESULT_STREAM)

    @app.get("/health")
    def health():
        return jsonify({
            "status": "ok",
            "redis": broker.ping(),
            "cache": cache.ping(),
            "postgres": stats_repo.ping(),
        })

    @app.get("/stats")
    def stats():
        chat_id = request.args.get("chat_id", type=int)
        cache_key = f"stats:{chat_id or 'all'}"
        cached = cache.get_stats(cache_key)
        if cached is not None:
            return jsonify({**cached, "cached": True})

        payload = {
            "chat_id": chat_id,
            "sentiment_pie": stats_repo.get_sentiment_distribution(chat_id),
            "sentiment_histogram": stats_repo.get_sentiment_by_day(chat_id),
            "problems": stats_repo.get_problem_categories(chat_id),
            "top_users": stats_repo.get_top_users(chat_id)
        }
        cache.set_stats(cache_key, payload)
        return jsonify({**payload, "cached": False})



    @app.get("/")
    def home():
        return jsonify({
            "service": "practice-maxbot-api",
            "endpoints": ["/health", "/stats?chat_id=<id>", "/results?limit=<n>"],
        })

    return app


def main() -> None:
    app = create_app()
    app.run(host=API_HOST, port=API_PORT)


if __name__ == "__main__":
    main()
