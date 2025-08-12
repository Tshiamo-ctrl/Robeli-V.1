# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install system deps (Postgres, xmlsec, etc.)
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential curl git ca-certificates pkg-config \
    libpq-dev libpq5 libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev \
    libxmlsec1-dev libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (for asset builds when enabled)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pre-copy requirement files to leverage docker cache
COPY requirements/ ./requirements/
COPY setup.py setup.cfg pyproject.toml* .coveragerc* mypy.ini pylintrc* /app/

# Install Python deps (runtime base)
RUN python -m pip install --upgrade pip \
    && awk '!/^mysqlclient==/' requirements/edx/base.txt > /tmp/base_no_mysql.txt \
    && sed -e '/^code-annotations==/d' -e '/^codejail-includes==/d' /tmp/base_no_mysql.txt > /tmp/reqs_postgres_py310.txt \
    && pip install --prefer-binary psycopg2-binary code-annotations==1.8.2 codejail-includes==1.0.0 \
    && pip install --prefer-binary -r /tmp/reqs_postgres_py310.txt

# Copy application source
COPY . /app

# Create an app user (non-root)
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

# Copy entrypoint and healthcheck scripts
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
COPY scripts/healthcheck.sh /app/scripts/healthcheck.sh
RUN chmod +x /app/scripts/entrypoint.sh /app/scripts/healthcheck.sh

ENV SERVICE=lms \
    PORT=8000 \
    NODE_ENV=production \
    WEB_CONCURRENCY=2 \
    LOG_LEVEL=info \
    RUN_MIGRATIONS=false \
    SKIP_ASSETS=true

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=5 CMD /app/scripts/healthcheck.sh || exit 1

USER appuser

# Default command
CMD ["/app/scripts/entrypoint.sh"]