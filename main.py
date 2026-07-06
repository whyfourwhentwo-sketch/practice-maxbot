from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN
from components.model.model_load import get_classifier
from components.model.model_train import train_classifier
from components.data.embeddings_handler import load_embedding_model
from components.bot.prediction import PredictionService
from components.bot.bot_handlers import handle_start, handle_message, handle_private_message


def setup_bot_data(app: Application) -> None:
    """Загружает сервисы в контекст бота."""
    embedding_model = load_embedding_model()
    classifier = get_classifier()
    prediction_service = PredictionService(embedding_model, classifier)

    app.bot_data['prediction_service'] = prediction_service


def create_application() -> Application:
    """Создает и настраивает приложение бота."""
    app = Application.builder().token(BOT_TOKEN).build()
    register_handlers(app)
    return app


def register_handlers(app: Application) -> None:
    """Регистрирует обработчики команд и сообщений."""
    app.add_handler(CommandHandler("start", handle_start))

    group_filter = filters.ChatType.GROUP | filters.ChatType.SUPERGROUP
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & group_filter,
        handle_message
    ))

    app.add_handler(MessageHandler(
        filters.ChatType.PRIVATE,
        handle_private_message
    ))


def main() -> None:
    """Главная функция запуска бота."""
    app = create_application()
    setup_bot_data(app)

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()