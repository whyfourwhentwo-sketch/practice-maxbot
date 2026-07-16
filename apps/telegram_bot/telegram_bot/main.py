import asyncio
import os

import telegram
from telegram import ReplyParameters
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.request import HTTPXRequest

#from telegram_bot.handlers import handle_start, handle_message, handle_private_message
from apps.telegram_bot.telegram_bot.handlers import handle_start, handle_message, handle_private_message
from shared.config import (
    BOT_TOKEN,
    INFERENCE_CONSUMER_GROUP,
    INFERENCE_RESULT_CONSUMER_GROUP,
    INFERENCE_RESULT_STREAM,
    INFERENCE_STREAM,
    LABELS
)
from shared.queue import MessageBroker, InferenceResultBatch


def setup_bot_data(app: Application) -> None:
    app.bot_data["inference_broker"] = MessageBroker(
        stream=INFERENCE_STREAM,
        group=INFERENCE_CONSUMER_GROUP,
    )
    app.bot_data["result_broker"] = MessageBroker(
        stream=INFERENCE_RESULT_STREAM,
        group=INFERENCE_RESULT_CONSUMER_GROUP,
    )
    app.bot_data["result_consumer_name"] = os.getenv("BOT_RESULT_CONSUMER_NAME", "bot-sender-1")


async def send_results_job(context) -> None:
    """Фоновая задача для чтения результатов из брокера и отправки их в Telegram."""
    app = context.application
    result_broker: MessageBroker = app.bot_data["result_broker"]
    consumer_name: str = app.bot_data["result_consumer_name"]

# в проде ответы бота не нужны
# Deprecated
    # print("[send_results_job] start")
    # try:
    #     entries = await asyncio.to_thread(
    #         result_broker.read_batch,
    #         consumer_name,
    #         8,
    #         200,
    #         InferenceResultBatch
    #     )
    #     print(f"[send_results_job] got {len(entries)} entries")

    #     if not entries:
    #         return

    #     ack_ids: list[str] = []
        
    #     for entry in entries:
    #         try:
    #             batch = entry.message
    #             messages = batch.messages
    #             predictions = batch.predictions
    #         except Exception as exc:
    #             print(f"[send_results_job] failed to parse entry {entry.entry_id}: {exc}")
    #             continue

    #         if not messages:
    #             print(f"[send_results_job] empty batch messages for entry {entry.entry_id}")
    #             continue

    #         for i, message in enumerate(messages):
    #             try:
    #                 # ответ бота в продакшене не нужен
    #                 await app.bot.send_message(
    #                     chat_id=message.chat_id,
    #                     text="\n".join(
    #                         f"{name} : {LABELS[name][predictions[name][i]]}"
    #                         for name in predictions
    #                     ),
    #                     reply_parameters=ReplyParameters(message_id=message.message_id)
    #                 )
    #                 print(f"[send_results_job] sent message {message.message_id} chat {message.chat_id}")
    #                 ack_ids.append(entry.entry_id)
    #             except telegram.error.TelegramError as exc:
    #                 print(f"[send_results_job] Failed to send result for chat {message.chat_id}: {exc}")
    #             except Exception as exc:
    #                 print(f"[send_results_job] unexpected error sending message {message.message_id}: {exc}")

    #     if ack_ids:
    #         await asyncio.to_thread(result_broker.ack, ack_ids)
    #         print(f"[send_results_job] acked {len(ack_ids)} entries")
    # except Exception as exc:
    #     print(f"[send_results_job] unexpected error: {exc}")
    # finally:
    #     print("[send_results_job] end")


def register_handlers(app: Application) -> None:
    """Регистрирует обработчики команд и сообщений."""
    app.add_handler(CommandHandler("start", handle_start))

    group_filter = filters.ChatType.GROUP | filters.ChatType.SUPERGROUP
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & group_filter,
        handle_message
    ))

    app.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & filters.TEXT,
        handle_private_message
    ))


def create_application() -> Application:
    """Создает и настраивает приложение бота."""
    request = HTTPXRequest(http_version="1.1")

    app = Application.builder().token(BOT_TOKEN).request(request).build()
    register_handlers(app)
    return app


def main() -> None:
    """Главная функция запуска бота."""
    app = create_application()
    setup_bot_data(app)
    app.job_queue.run_repeating(send_results_job, interval=2.0, first=1.0)

    print("Бот запущен и слушает сообщения...")

    app.run_polling(
        bootstrap_retries=10,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()