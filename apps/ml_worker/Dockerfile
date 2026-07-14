FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==2.1.1

COPY pyproject.toml poetry.lock ./

RUN mkdir -p packages/shared && echo '[tool.poetry]\nname = "shared"\nversion = "0.1.0"' > packages/shared/pyproject.toml

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

COPY packages/shared packages/shared

RUN pip install --no-cache-dir --force-reinstall ./packages/shared

COPY apps/ml_worker apps/ml_worker
COPY data data

ENV PYTHONPATH=/app/apps/ml_worker
ENV DATA_DIR=/app/data

CMD ["python", "-m", "ml_worker.worker"]
