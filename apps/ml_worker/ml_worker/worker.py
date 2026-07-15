import asyncio

import os
import signal

from shared.config import (
    INFERENCE_RESULT_CONSUMER_GROUP,
    INFERENCE_RESULT_STREAM,
    INFERENCE_STREAM,
    INFERENCE_CONSUMER_GROUP,
    ML_BATCH_SIZE,
)
from shared.db import AnalysisRecord, StatsRepository
from shared.db.repository import SENTIMENT_LABELS
from shared.queue import InferenceMessage

from shared.queue.broker import StreamEntry, MessageBroker
from shared.queue import InferenceResultBatch, InferenceResultMessageTest
from .model_loader import load_classifiers, load_embedding_model
from .prediction import PredictionService


def _clean_text(text: str) -> str:
    return " ".join(text.split())


def _build_analysis_record(
    message: InferenceMessage,
    useful_label: int,
    sentiment_label: int,
    usefulness_confidence: float | None,
    sentiment_confidence: float | None,
) -> AnalysisRecord:
    return AnalysisRecord(
        platform=message.platform,
        platform_chat_id=str(message.chat_id),
        chat_name=message.chat_name or str(message.chat_id),
        platform_user_id=str(message.platform_user_id or message.user_name),
        user_name=message.user_name or "unknown",
        platform_message_id=str(message.message_id),
        raw_text=message.text,
        cleaned_text=_clean_text(message.text),
        is_useful=useful_label == 0,
        usefulness_confidence=usefulness_confidence,
        sentiment=SENTIMENT_LABELS.get(sentiment_label),
        sentiment_confidence=sentiment_confidence,
    )


class MLWorker:
    def __init__(self) -> None:
        self._consumer_name = os.getenv("ML_CONSUMER_NAME", "worker-1")
        self._batch_size = ML_BATCH_SIZE
        self._request_broker = MessageBroker(
            stream=INFERENCE_STREAM,
            group=INFERENCE_CONSUMER_GROUP,
        )
        self._result_broker = MessageBroker(
            stream=INFERENCE_RESULT_STREAM,
            group=INFERENCE_RESULT_CONSUMER_GROUP,
        )
        self._stats = StatsRepository()
        self._prediction_service: PredictionService | None = None
        self._running = True

    def load_models(self) -> None:
        print("Loading embedding model and classifier...", flush=True)
        embedding_model = load_embedding_model()
        print("Models loaded.", flush=True)
        self._prediction_service = PredictionService(embedding_model, load_classifiers())
        self._stats.connect()
        print("Database connected.", flush=True)

    async def run(self) -> None:
        if self._prediction_service is None:
            raise RuntimeError("Models are not loaded. Call load_models() first.")

        print(f"ML worker started (consumer={self._consumer_name}, batch_size={self._batch_size})")

        while self._running:
            try:
                entries = await asyncio.to_thread(
                    self._request_broker.read_batch,
                    message_model=InferenceMessage,
                    consumer_name=self._consumer_name,
                    count=self._batch_size,
                    block_ms=5000,
                )

                if not entries:
                    continue

                await asyncio.to_thread(self._process_batch, entries)

            except Exception as e:
                print(f"Error in ML worker loop: {e}")
                await asyncio.sleep(1)

    def _process_batch(self, entries: list[StreamEntry]) -> None:
        texts = [entry.message.text for entry in entries]
        predictions = self._prediction_service.predict_batch(texts)
        if predictions is None:
            return

        records: list[AnalysisRecord] = []
        batch_messages = []
        for i, entry in enumerate(entries):
            message = entry.message
            batch_messages.append(
                InferenceResultMessageTest(
                    message_id=message.message_id,
                    chat_id=message.chat_id,
                )
            )
            records.append(
                _build_analysis_record(
                    message=message,
                    useful_label=predictions["useful"][i],
                    sentiment_label=predictions["sentiment"][i],
                    usefulness_confidence=predictions.get("useful_confidence", [None])[i],
                    sentiment_confidence=predictions.get("sentiment_confidence", [None])[i],
                )
            )

        self._result_broker.publish(
            InferenceResultBatch(messages=batch_messages, predictions=predictions)
        )
        self._stats.save_batch(records)
        self._request_broker.ack([entry.entry_id for entry in entries])

    def stop(self) -> None:
        self._running = False


def _setup_signal_handlers(worker: MLWorker) -> None:
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, worker.stop)
        except NotImplementedError:
            pass


async def _async_main() -> None:
    worker = MLWorker()
    worker.load_models()
    _setup_signal_handlers(worker)
    await worker.run()


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
