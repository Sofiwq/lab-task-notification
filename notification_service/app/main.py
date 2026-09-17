from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.models import Task
from app.notifier import send_notification

app = FastAPI(
    title="Notification Service",
    description="Сервис уведомлений для «Умного планировщика задач»",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """Простой healthcheck — удобно для интеграционных тестов."""
    return {"status": "ok"}


@app.post(
    "/api/webhooks/task_created",
    status_code=status.HTTP_200_OK,
)
def task_created_webhook(task: Task):
    """
    Принимает событие о создании задачи и эмулирует отправку уведомления.
    """
    send_notification(task)
    return {"status": "received", "task_id": str(task.id)}