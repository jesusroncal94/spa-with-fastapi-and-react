from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Task:
    id: str
    title: str
    done: bool
    created_at: datetime
