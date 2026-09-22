from fastapi import APIRouter, status

from taskboard.api.dependencies import ServiceDep
from taskboard.api.schemas import CreateTaskRequest, TaskResponse, UpdateTaskRequest

router = APIRouter(prefix="/api")


@router.get("/health", tags=["monitoring"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/tasks", tags=["tasks"])
async def list_tasks(service: ServiceDep) -> list[TaskResponse]:
    tasks = await service.list_tasks()
    return [TaskResponse.from_domain(task) for task in tasks]


@router.post("/tasks", status_code=status.HTTP_201_CREATED, tags=["tasks"])
async def create_task(payload: CreateTaskRequest, service: ServiceDep) -> TaskResponse:
    task = await service.create_task(payload.title)
    return TaskResponse.from_domain(task)


@router.patch("/tasks/{task_id}", tags=["tasks"])
async def update_task(
    task_id: str, payload: UpdateTaskRequest, service: ServiceDep
) -> TaskResponse:
    task = await service.update_task(task_id, title=payload.title, done=payload.done)
    return TaskResponse.from_domain(task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
async def delete_task(task_id: str, service: ServiceDep) -> None:
    await service.delete_task(task_id)
