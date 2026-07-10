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

Запуск обучения моделей, требует Excel файл `data/excel/data_ml.xlsx`.

```bash
# -t --train
poetry run python main.py -t
```

Или с указанием пользовательского файла:

```bash
# -f --file
poetry run python main.py -t -f path/to/file.xlsx
```
В данный момент -f не работает сам по себе

**Результат:** 
Модели сохраняются в `data/models/` согласно меткам, перечисленным в конфиге `shared/config.py` 

```text
LABELS = { # модели создаются на базе этого параметра
    "useful": ["да", "нет"],
    "sentiment": ["+", "-", "="],
}

Сохраненные модели (при наличии данных столбцов в таблице): useful.pkl, sentiment.pkl
```

Метки, не указанные в конфиге или несуществующие в таблице будут проигнорированы

**Аргументы:**
- `-t, --train` — запустить обучение моделей
- `-f, --file` — путь к файлу с данными (опционально)

## Docker

```bash
docker compose up --build
```
- API: http://localhost:5000/health
- Redis: `localhost:6379`
- Postgres: `localhost:5432

ВНИМАНИЕ: Бот внутри докера работать не будет 
