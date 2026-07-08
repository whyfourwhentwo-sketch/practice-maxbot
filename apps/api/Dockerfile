FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.1.1

COPY pyproject.toml poetry.lock ./
COPY packages/shared packages/shared

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root \
    && pip install --no-cache-dir ./packages/shared

COPY apps/api apps/api

ENV PYTHONPATH=/app/apps/api

CMD ["python", "-m", "api.app"]
