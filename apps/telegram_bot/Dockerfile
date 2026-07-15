FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.1.1

COPY pyproject.toml poetry.lock ./

RUN mkdir -p packages/shared && echo '[tool.poetry]\nname = "shared"\nversion = "0.1.0"' > packages/shared/pyproject.toml

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

COPY packages/shared packages/shared

RUN pip install --no-cache-dir --force-reinstall ./packages/shared
COPY apps/telegram_bot apps/telegram_bot

ENV PYTHONPATH=/app/apps/telegram_bot

CMD ["python", "-m", "telegram_bot.main"]
