FROM node:22-slim AS web-deps

WORKDIR /web

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund


FROM web-deps AS web-dev

COPY frontend/ ./

CMD ["npm", "run", "dev"]


FROM web-deps AS web-build

COPY frontend/ ./
RUN npm run build


FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS api-build

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY backend/src ./src
RUN uv sync --frozen --no-dev


FROM api-build AS api-dev

COPY backend/tests ./tests
RUN uv sync --frozen && mkdir -p /app/data

CMD ["uv", "run", "pytest", "-q"]


FROM python:3.12-slim-bookworm AS runtime

RUN groupadd --system app && useradd --system --gid app --create-home app

WORKDIR /app

COPY --from=api-build --chown=app:app /app/.venv ./.venv
COPY --from=api-build --chown=app:app /app/src ./src
COPY --from=web-build --chown=app:app /web/dist ./static

RUN mkdir -p /app/data && chown app:app /app/data

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    STATIC_DIRECTORY=/app/static \
    DATABASE_URL=sqlite+aiosqlite:///./data/taskboard.db \
    CORS_ORIGINS=[]

USER app

EXPOSE 8000

CMD ["uvicorn", "taskboard.main:app", "--host", "0.0.0.0", "--port", "8000"]
