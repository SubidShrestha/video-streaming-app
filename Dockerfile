# === Build stage ===
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.2

# Install build tools, ffmpeg, netcat, curl
RUN apt-get update && apt-get install -y \
  build-essential libpq-dev curl ffmpeg netcat-openbsd

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Copy only dependency files first (for caching)
COPY ./pyproject.toml ./poetry.lock* /app/

RUN chmod 644 ./pyproject.toml ./poetry.lock

# Install dependencies (excluding the source code)
RUN poetry config virtualenvs.create false && \
poetry install --no-root --only main

# === Runtime stage ===
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

# Only install minimal runtime deps
RUN apt-get update && apt-get install -y \
  build-essential libpq-dev curl ffmpeg netcat-openbsd

WORKDIR /app

# Copy installed packages from the base stage
COPY --from=base /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=base /usr/local/bin/ /usr/local/bin/

# Set PYTHONPATH so the code in 'src/' can be found
ENV PYTHONPATH=/app/src

COPY ./src /app/src

# Copy entrypoint script and make it executable
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the application port
EXPOSE 8000

# Start with the entrypoint
ENTRYPOINT ["/entrypoint.sh"]