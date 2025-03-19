ARG PYVER=3.13
FROM python:${PYVER}-slim AS builder

WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get -qq update > /dev/null && \
    apt-get -qq install -y --no-install-recommends \
        build-essential \
        curl \
        # psycopg2 build dependencies
        libpq-dev > /dev/null

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - > /dev/null
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies to .venv to isolate them from the system python
COPY pyproject.toml poetry.lock ./
RUN python -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"
RUN poetry install --no-root --without dev --quiet


FROM python:${PYVER}-slim AS final

WORKDIR /app


# Install required runtime dependencies
RUN apt-get -qq update > /dev/null && \
    apt-get -qq install -y --no-install-recommends \
        # for healthcheck
        curl \
        # psycopg2 runtime dependencies
        libpq5 > /dev/null \
    && apt-get -qq clean && rm -rf /var/lib/apt/lists/*

# Copy .venv from the builder stage
COPY --from=builder /app/.venv ./.venv
ENV PATH="/app/.venv/bin:$PATH"
# Copy the application code
COPY . .

# Expose the Flask port
EXPOSE 5000
# Run with gunicorn
# add --preload to prevent db.create_all() race condition
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()", "--preload", "--workers", "9"]
# CMD ["flask", "run", "--host", "0.0.0.0", "--debug"]
# CMD ["tail", "-f", "/dev/null"]
