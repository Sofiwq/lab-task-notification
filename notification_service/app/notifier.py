import logging
from pathlib import Path

from app.models import Task

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "notifications.log"

logger = logging.getLogger("notification_service")
logger.setLevel(logging.INFO)

# Чтобы не дублировать хендлеры при повторном импорте
if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def send_notification(task: Task) -> None:
    """
    Эмулирует отправку уведомления пользователю.
    В реальной системе здесь был бы вызов email/SMS/push-провайдера.
    """
    message = (
        f"Уведомление: создана новая задача "
        f"[{task.id}] '{task.title}' (status={task.status.value}, "
        f"created_at={task.created_at.isoformat()})"
    )
    logger.info(message)