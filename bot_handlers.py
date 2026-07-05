from telegram import Update
from telegram.ext import CallbackContext

from utils import format_prediction


async def handle_start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start."""
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"Привет {user_name}!")


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик текстовых сообщений в чате."""
    text, sender = get_message_details(update)
    print(f"{sender}: {text}")

    prediction_service = context.bot_data['prediction_service']
    prediction = prediction_service.predict(text)
    response = format_prediction(prediction)

    print(f"Бот: {response}")
    await update.message.reply_text(response)


async def handle_private_message(update: Update, context: CallbackContext) -> None:
    """Игнорим)"""
    text, sender = get_message_details(update)
    print(f"[Сообщение в личку бота] {sender}: {text}")
    return


def get_message_details(update: Update) -> tuple[str, str]:
    text = update.message.text
    sender = update.message.from_user.first_name
    return text, sender
