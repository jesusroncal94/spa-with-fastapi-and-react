class TaskboardError(Exception):
    pass


class TaskNotFoundError(TaskboardError):
    def __init__(self, task_id: str) -> None:
        super().__init__(f"No task exists with id '{task_id}'")
        self.task_id = task_id
