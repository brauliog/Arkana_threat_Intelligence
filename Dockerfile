FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY arkana ./arkana

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ".[dev]"

FROM base AS dev

EXPOSE 8000

CMD ["uvicorn", "arkana.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS prod

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "arkana.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
