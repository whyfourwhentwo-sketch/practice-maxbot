import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8919976232:AAFcGrtP9VWKo3I4WK9Ss2DhUASoFWzvo3U"

async def start(update: Update, context: CallbackContext):
    
    text = (
        f"Привет {update.effective_user.first_name}!"
    )
    
    await update.message.reply_text(text)
    

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    sender = update.message.from_user.first_name
    
    print(f"{sender}: {text}")
    
    

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот должен быть запущен")
    app.run_polling()
    
    

if __name__ == "__main__":
    main()
