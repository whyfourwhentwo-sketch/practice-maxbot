# Бот-градусник

Telegram-бот классифицирует сообщения в групповых чатах как «Полезное» / «Бесполезное».

## Структура

```
practice-maxbot/
├── apps/
│   ├── telegram-bot/
│   ├── ml-worker/
│   └── api/
├── packages/shared/    
├── training/            
├── data/               
├── docker-compose.yml
└── main.py             
```

## Быстрый старт (локально)

### 1. Зависимости

```bash
poetry install
```

### 2. Переменные окружения

```bash
cp .env-example .env
# Заполните TOKEN
```

### 3. Redis

```bash
docker compose up redis -d
```

### 4. Запуск сервисов (3 терминала)

```bash
# Терминал 1 — бот
poetry run python main.py

# Терминал 2 — ML worker
set PYTHONPATH=apps/ml_worker
poetry run python -m ml_worker.worker

# Терминал 3 — API
set PYTHONPATH=apps/api
poetry run python -m api.app
```

На Linux/macOS замените `set` на `export`.

### 5. Обучение модели

```bash
poetry run python training/train.py
```

Требует `data/excel/data_ml.xlsx`. Результат: `data/models/classifier.pkl`.

## Docker

```bash
docker compose up --build
```
- API: http://localhost:5000/health
- Redis: `localhost:6379`
- Postgres: `localhost:5432

ВНИМАНИЕ: Бот внутри докера работать не будет 
