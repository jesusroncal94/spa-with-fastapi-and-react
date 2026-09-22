from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from taskboard.domain.errors import TaskNotFoundError
from taskboard.domain.models import Task
from taskboard.domain.repository import TaskRepository


class TaskboardService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def list_tasks(self) -> list[Task]:
        return await self._repository.list_all()

    async def create_task(self, title: str) -> Task:
        task = Task(
            id=str(uuid4()),
            title=title.strip(),
            done=False,
            created_at=datetime.now(UTC),
        )
        await self._repository.add(task)
        return task

    async def update_task(self, task_id: str, *, title: str | None, done: bool | None) -> Task:
        task = await self._require(task_id)
        updated = replace(
            task,
            title=task.title if title is None else title.strip(),
            done=task.done if done is None else done,
        )
        await self._repository.replace(updated)
        return updated

    async def delete_task(self, task_id: str) -> None:
        if not await self._repository.remove(task_id):
            raise TaskNotFoundError(task_id)

    async def _require(self, task_id: str) -> Task:
        task = await self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task
