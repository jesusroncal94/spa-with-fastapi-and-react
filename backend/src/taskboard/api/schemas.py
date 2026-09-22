from datetime import datetime

from pydantic import BaseModel, Field

from taskboard.domain.models import Task


class CreateTaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class UpdateTaskRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    done: bool | None = None


class TaskResponse(BaseModel):
    id: str
    title: str
    done: bool
    created_at: datetime

    @classmethod
    def from_domain(cls, task: Task) -> "TaskResponse":
        return cls(id=task.id, title=task.title, done=task.done, created_at=task.created_at)
