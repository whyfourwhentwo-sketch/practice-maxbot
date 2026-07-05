from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

MODEL = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def save_embeddings(embeddings, labels):
    np.savez('data.npz', embeddings=embeddings, labels=labels)


def create_embeddings():
    wb = load_workbook('data_ml.xlsx')
    sheet = wb.active
    phrase = []
    is_useful = []
    for row in sheet['A1:D311']:
        phrase.append(str(row[0].value))
        is_useful.append(1 if row[3].value == 'да' else 0)
        
    
    embeddings = MODEL.encode(phrase[1::], show_progress_bar=True)

    return np.array(embeddings), np.array(is_useful[1::])

def load_data():
    try:
        data = np.load('data.npz', allow_pickle=True)
        embeddings = data['embeddings']
        labels = data['labels']
        
    except FileNotFoundError:
        embeddings, labels = create_embeddings()
        save_embeddings(embeddings, labels)
        
    return embeddings, labels


def model_train():
    embeddings, labels = load_data()
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Labels shape: {labels.shape}")
    
    X_train, X_test, y_train, y_test = train_test_split(embeddings, labels, test_size=0.2, random_state=42)
    clf = LogisticRegression(class_weight='balanced', max_iter=1000)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    
    return clf
    

async def start(update: Update, context: CallbackContext):
    text = (
        f"Привет {update.effective_user.first_name}!"
    )
    
    await update.message.reply_text(text)
    

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    sender = update.message.from_user.first_name
    
    print(f"{sender}: {text}")
    
    embedding = MODEL.encode([text])
    prediction = context.bot_data['model'].predict(embedding)
    response = "Полезное" if prediction[0] == 1 else "Бесполезное"
    
    await update.message.reply_text(response)
    

def load_model():
    try:
        model = joblib.load('model.pkl')
        
    except FileNotFoundError:
        model = model_train()
        joblib.dump(model, 'model.pkl')
        
    return model
    
def main():
    model = load_model()
    
    app = Application.builder().token(TOKEN).build()
    app.bot_data['model'] = model
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))\
        
    print("Бот должен быть запущен")
    app.run_polling()
    
    
if __name__ == "__main__":
    main()