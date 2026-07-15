from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
from .cache import StatsCache
from shared.config import API_HOST, API_PORT, INFERENCE_RESULT_STREAM, INFERENCE_RESULT_CONSUMER_GROUP
from shared.db import StatsRepository
from shared.queue import InferenceResultBatch, MessageBroker
from shared.queue.schemas import APIResponse
# WebSocket (flask-socketio) будет добавлен, когда появится фронтенд.
# Бэкенд сможет пушить события stats:updated при записи в Postgres.


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    stats_repo = StatsRepository()
    stats_repo.connect()
    cache = StatsCache()
    broker = MessageBroker(
        stream=INFERENCE_RESULT_STREAM
    )

    
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
        print(chat_id)
        cached = cache.get_stats(cache_key)
        if cached is not None:
            return jsonify({**cached, "cached": True})

        # payload = stats_repo.get_chat_stats(chat_id)
        # cache.set_stats(cache_key, payload)
        # return jsonify({**payload, "cached": False})
        
        try:
            entries = broker.read_stream()
            predictions : list[dict[str, list[int]]] = [] # Пиздец
            print(type(entries))
            for entry in entries:
                predictions.append(entry.message.predictions)
            response = jsonify({"response": predictions})
            return response
        except Exception as e:
                print(f"Error in ML worker loop: {e}")
                
        response = APIResponse(text="Иди нахуй со своим апи")
        response_dict = response.model_dump(mode="json")

        return jsonify({**response_dict, "cached": False})

    @app.get("/results")
    def results():
        """Return recent inference results from Redis.

        Query params:
        - limit: number of entries to return (default 50)
        - mode: "stream" (default) or "group". "stream" uses XRANGE/XREVRANGE (read-only log).
                "group" uses XREADGROUP and requires a consumer name and optionally a group name.
        - consumer_name: name of the consumer when using mode=group (default: api-reader-1)
        - group: consumer group name when using mode=group (default: INFERENCE_RESULT_CONSUMER_GROUP + '-api')
        - start_id: stream start id for paging when using mode=stream (default: '-')
        """
        limit = request.args.get("limit", default=50, type=int)
        mode = request.args.get("mode", default="stream")

        if mode == "group":
            consumer_name = request.args.get("consumer_name", default="api-reader-1")
            group = request.args.get("group", default=INFERENCE_RESULT_CONSUMER_GROUP + "-api")
            broker = MessageBroker(stream=INFERENCE_RESULT_STREAM, group=group)

            # non-blocking read from the consumer group
            entries = broker.read_batch(consumer_name=consumer_name, count=limit, block_ms=0, message_model=InferenceResultBatch)

        else:
            # default: read-only log view (does not affect consumer groups)
            start_id = request.args.get("start_id", default="-")
            broker = MessageBroker(stream=INFERENCE_RESULT_STREAM)
            entries = broker.read_stream(count=limit, start=start_id, reverse=True, message_model=InferenceResultBatch)

        return jsonify({
            "stream": INFERENCE_RESULT_STREAM,
            "mode": mode,
            "count": len(entries),
            "results": [
                {
                    "entry_id": entry.entry_id,
                    **entry.message.model_dump(),
                }
                for entry in entries
            ],
        })

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
