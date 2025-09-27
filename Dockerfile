FROM astral/uv:python3.12-bookworm-slim

# Install PostgreSQL client libraries
RUN apt-get update && apt-get install -y \
  libpq-dev

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1

COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock
COPY ./README.md /app/README.md

RUN --mount=type=cache,target=/root/.cache/uv uv sync --no-install-project

COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./src /app/src
RUN --mount=type=cache,target=/root/.cache/uv uv sync

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "src/run.py"]
