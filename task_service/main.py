from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
import uuid
import httpx
import logging

from models import TaskCreate, Task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("task_service")

app = FastAPI(title="Task Service")

NOTIFICATION_URL = "http://localhost:8002/api/webhooks/task_created"

tasks_db: dict[str, Task] = {}


def send_webhook(task: Task):
    """Отправка вебхука с одной повторной попыткой. Не роняет сервис."""
    payload = task.model_dump()
    for attempt in (1, 2):
        try:
            r = httpx.post(NOTIFICATION_URL, json=payload, timeout=3.0)
            if r.status_code == 200:
                logger.info(f"Webhook OK for task {task.id}")
                return
            logger.warning(f"Webhook returned {r.status_code} (attempt {attempt})")
        except Exception as e:
            logger.error(f"Webhook failed (attempt {attempt}): {e}")
    logger.error(f"Webhook permanently failed for task {task.id}")


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="title is required")

    task = Task(
        id=str(uuid.uuid4()),
        title=payload.title,
        description=payload.description,
        status=payload.status,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    tasks_db[task.id] = task
    logger.info(f"Task created: {task.id}")
    send_webhook(task)
    return task


@app.get("/api/tasks", response_model=list[Task])
def list_tasks():
    return list(tasks_db.values())


@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]