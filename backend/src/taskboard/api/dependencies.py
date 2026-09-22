from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from taskboard.domain.services import TaskboardService
from taskboard.infrastructure.sql_task_repository import SqlTaskRepository


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_service(session: Annotated[AsyncSession, Depends(get_session)]) -> TaskboardService:
    return TaskboardService(SqlTaskRepository(session))


ServiceDep = Annotated[TaskboardService, Depends(get_service)]
