# Бот-градусник

Telegram-бот классифицирует сообщения в групповых чатах как «Полезное» / «Бесполезное».

## Структура

```
practice-maxbot/
├── apps/
│   ├── api/
│   │   └── api/
│   ├── ml_worker/
│   │   └── ml_worker/
│   └── telegram_bot/
│       └── telegram_bot/
├── packages/
│   └── shared/
│       └── shared/
├── training/
├── data/
│   ├── excel/
│   ├── machine/
│   └── models/
├── frontend_charts/
│   ├── public/
│   └── src/
│       └── components/
├── docker-compose.yml
├── main.py
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Быстрый старт (локально)

### 1. Зависимости

```bash
poetry install  # бэк
npm install     # фронт
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
poetry run python main.py -b

# Терминал 2 — ML worker
poetry run python main.py -w

# Терминал 3 — API
poetry run python main.py -a
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

### 6. Аргументы
- `-t, --train` — запустить обучение моделей
- `-f, --file` — путь к файлу с данными (опционально, ничего не сделает без `-t`)
- `-w, --worker` — запуск сервиса классификации сообщений
- `-a, --api` — запуск сервиса API для фронтенда
- `-b, --bot` — запуск сервиса с Telegram ботов

Пожалуйста, не смешивайте аргументы (кроме `-t` и `-f`)


### 7. Фроентенд (WIP)

В данный момент находится в околозачаточном состоянии.

Запуск через HTTP-сервер (рекомендуется):
```bash
cd frontend
python -m http.server 5500
```

Затем открой в браузере `http://127.0.0.1:5500/index.html`.

Если фронтенд и API работают с разных портов, нужно включить CORS на API-сервере.
## Docker (Может не работать)

```bash
docker compose up --build
```
- API: http://localhost:5000/health
- Redis: `localhost:6379`
- Postgres: `localhost:5432

ВНИМАНИЕ: Бот внутри докера работать не будет 
