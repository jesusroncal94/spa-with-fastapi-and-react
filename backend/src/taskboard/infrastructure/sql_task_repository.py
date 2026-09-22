from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from taskboard.domain.models import Task
from taskboard.infrastructure.database import TaskRecord, as_utc


class SqlTaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Task]:
        statement = select(TaskRecord).order_by(TaskRecord.created_at.desc())
        records = await self._session.scalars(statement)
        return [self._to_domain(record) for record in records]

    async def add(self, task: Task) -> None:
        self._session.add(
            TaskRecord(
                id=task.id,
                title=task.title,
                done=task.done,
                created_at=task.created_at,
            )
        )
        await self._session.flush()

    async def get(self, task_id: str) -> Task | None:
        record = await self._session.get(TaskRecord, task_id)
        return self._to_domain(record) if record is not None else None

    async def replace(self, task: Task) -> None:
        record = await self._session.get(TaskRecord, task.id)
        if record is None:
            return
        record.title = task.title
        record.done = task.done
        await self._session.flush()

    async def remove(self, task_id: str) -> bool:
        result = await self._session.execute(delete(TaskRecord).where(TaskRecord.id == task_id))
        await self._session.flush()
        return result.rowcount > 0

    @staticmethod
    def _to_domain(record: TaskRecord) -> Task:
        return Task(
            id=record.id,
            title=record.title,
            done=record.done,
            created_at=as_utc(record.created_at),
        )
