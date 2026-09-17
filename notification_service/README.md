# Notification Service

Микросервис уведомлений для «Умного планировщика задач».
Принимает событие о создании задачи и эмулирует отправку уведомления
(запись в `logs/notifications.log` и в консоль).

## Стек

- Python 3.11
- FastAPI + Uvicorn
- Pydantic
- Pytest

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001