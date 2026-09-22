import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from taskboard.api.routes import router
from taskboard.config import Settings, get_settings
from taskboard.domain.errors import TaskNotFoundError
from taskboard.infrastructure.database import (
    build_engine,
    build_session_factory,
    create_schema,
)
from taskboard.static import mount_single_page_app


async def handle_task_not_found(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    logging.basicConfig(level=settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = build_engine(settings.database_url)
        await create_schema(engine)
        app.state.session_factory = build_session_factory(engine)
        yield
        await engine.dispose()

    app = FastAPI(title="Taskboard", version="1.0.0", lifespan=lifespan)
    app.state.settings = settings
    app.add_exception_handler(TaskNotFoundError, handle_task_not_found)

    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(router)

    if settings.static_directory is not None:
        mount_single_page_app(app, settings.static_directory)

    return app


app = create_app()
