from flask import Flask, jsonify, request
from flask_cors import CORS

from .cache import StatsCache
from shared.config import API_HOST, API_PORT, INFERENCE_RESULT_STREAM, INFERENCE_RESULT_CONSUMER_GROUP
from shared.db import StatsRepository
from shared.queue import MessageBroker
from datetime import datetime

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
        chat_id = request.args.get("chat_id", type=str)
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")
        
        if date_from and date_to:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            
        print(date_from)
        print(date_to)
        
        cache_key = f"stats:{f"{chat_id}-{date_from}-{date_to}" or 'all'}"
        cached = cache.get_stats(cache_key)
        if cached is not None:
            return jsonify({**cached, "cached": True})

        payload = {
            "chat_id": chat_id,
            "sentiment_pie": stats_repo.get_sentiment_distribution(chat_id, date_from, date_to),
            "sentiment_histogram": stats_repo.get_sentiment_by_day(chat_id, date_from, date_to),
            "problems": stats_repo.get_problem_categories(chat_id, date_from, date_to),
            "top_users": stats_repo.get_top_users(chat_id, date_from, date_to),
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
