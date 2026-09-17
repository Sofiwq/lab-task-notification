from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"


class Task(BaseModel):
    id: UUID
    title: str = Field(..., min_length=1)
    description: str = ""
    status: TaskStatus
    created_at: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Купить молоко",
                "description": "Не забыть 2.5%",
                "status": "new",
                "created_at": "2026-09-17T09:50:00Z",
            }
        }
    }