from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = ""
    status: TaskStatus = TaskStatus.new


class Task(TaskCreate):
    id: str
    created_at: str
