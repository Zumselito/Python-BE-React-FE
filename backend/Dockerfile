# ── base ──────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install -e .

# ── dev ───────────────────────────────────────────────────────────────────────
FROM base AS dev
RUN pip install -e ".[dev]"
COPY . .
# CMD set via docker-compose

# ── test ──────────────────────────────────────────────────────────────────────
FROM dev AS test
RUN pytest --cov=app --cov-report=term-missing --cov-fail-under=80

# ── prod ──────────────────────────────────────────────────────────────────────
FROM base AS prod
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
