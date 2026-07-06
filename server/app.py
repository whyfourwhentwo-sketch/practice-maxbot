from flask import Flask, request
from cloudpub_python_sdk import Connection, Protocol, Auth
from flask import Flask, request, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv


# --------------- ___Загружаем переменные из .env___ -------------------------------------
load_dotenv()
# --- Читаем секреты из переменных окружения ---
CLOUDPUB_EMAIL = os.getenv('CLOUDPUB_EMAIL')
CLOUDPUB_PASSWORD = os.getenv('CLOUDPUB_PASSWORD')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
#
# --- Проверка, что секреты загружены ---
if not all([CLOUDPUB_EMAIL, CLOUDPUB_PASSWORD]):
    print("ОШИБКА: Не найдены CLOUDPUB_EMAIL или CLOUDPUB_PASSWORD в .env")
    exit(1)
# --------------- ___Загружаем переменные из .env___ -------------------------------------


# --------------- ___Настройка CloudPub___ ----------------------------------------------
# Создаем подключение, используя ваши учетные данные от cloudpub.ru
conn = Connection(
    email=CLOUDPUB_EMAIL,  # Замените на ваш email
    password=CLOUDPUB_PASSWORD         # Замените на ваш пароль
)
#
# Публикуем ваш локальный Flask-сервер
# Предполагается, что ваш сервер запущен на localhost:5000
endpoint = conn.publish(
    Protocol.HTTP,          # Протокол вашего сервера
    "localhost:5000",       # Локальный адрес и порт
    "Мой Flask бот",       # Название сервиса (опционально)
    Auth.NONE              # Тип аутентификации (опционально)
)
# --------------- ___Настройка CloudPub___ ----------------------------------------------


app = Flask(__name__)

# Получаем публичный URL, который будет использоваться для вебхука
public_url = endpoint.url
print(f"Сервис опубликован по адресу: {public_url}")
# URL для вебхука Telegram (добавляем ваш endpoint, например, /webhook)
webhook_url = public_url + "/webhook"
print(f"Используйте этот URL для настройки вебхука: {webhook_url}")


@app.route('/webhook', methods=['POST'])
    
    

@app.route('/', methods=['GET'])
def home():
    return "🚀 Сервер работает! Вебхук активен."




if __name__ == '__main__':
    # Запускаем Flask-сервер
    app.run(port=5000, debug=True)
