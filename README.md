# Бот-градусник

Микросервисный ИИ сервис мониторинга настроения, проблем и потребностей жителей ЖКХ за счет анализа домовых чатов, а также подведения статистики по чатам 

## Структура

```
.
├── apps/
│   ├── api/
│   │   └── api
│   ├── ml_worker/
│   │   └── ml_worker/
│   └── telegram_bot/
│       └── telegrambot/
├── data/
│   ├── excel/
│   ├── machine/
│   └── models/
├── frontend_charts/
│   ├── public/
│   └── src/
│       └── components/
├── packages/
│   └── shared/
│       ├── db/
│       ├── queue/
│       └── utils/
├── training/
│   ├── data/
│   └── model/
├── .env_example
├── build_ml_worker.log
├── docker-compose.yml
├── main.py
├── poetry.lock
├── README.md
└── TODO.md
```

## Быстрый старт (локально)

### 1. Зависимости

```bash
poetry install # бэк
npm install    # фронт
```

### 2. Переменные окружения

```bash
cp .env-example .env
# Заполните TOKEN
```

### 3. Redis

Для локального запуска подойдет memurai


Запуск через докер

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

# Терминал 4 — Фронтенд
cd forntend_charts
npm run
```

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


### 7. Фронтенд

Запуск через npm:
```bash
cd frontend_charts
npm run

# http://localhost:3000/
# npm откроет страницу самостоятельно
```

## Docker (Может не работать)

```bash
docker compose up --build
```
- API: http://localhost:5000/health
- Redis: `localhost:6379`
- Postgres: `localhost:5432

ВНИМАНИЕ: Бот внутри докера работать не будет 
