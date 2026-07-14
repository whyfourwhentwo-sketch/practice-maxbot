from datetime import datetime, timezone

from telegram import Update
from telegram.ext import CallbackContext

from shared.queue import InferenceMessage, MessageBroker


def get_broker(context: CallbackContext) -> MessageBroker:
    return context.bot_data["inference_broker"]


async def handle_start(update: Update, context: CallbackContext) -> None:
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"Привет {user_name}!")


async def handle_message(update: Update, context: CallbackContext) -> None:
    try:
        text, sender = get_message_details(update)
        print(f"[handle_message] received message from {sender}: {text}")

        broker = get_broker(context)
        print("[handle_message] got broker, preparing InferenceMessage")

        message = InferenceMessage(
            message_id=update.message.message_id,
            chat_id=update.effective_chat.id,
            text=text,
            user_name=sender,
            enqueued_at=datetime.now(timezone.utc).isoformat(),
        )

        print("[handle_message] publishing inference job")
        entry_id = broker.publish(message)
        print(f"[handle_message] Enqueued inference job {entry_id} for chat {message.chat_id}")
    except Exception as exc:
        print(f"[handle_message] error: {exc}")
        raise


async def handle_private_message(update: Update, context: CallbackContext) -> None:
    text, sender = get_message_details(update)
    print(f"[Сообщение в личку бота] {sender}: {text}")


def get_message_details(update: Update) -> tuple[str, str]:
    text = update.message.text
    sender = update.message.from_user.first_name
    return text, sender
