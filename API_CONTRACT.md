# API Contract: Умный планировщик задач

## 1. Схема данных Task

```json
{
  "id": "uuid (string)",
  "title": "string",
  "description": "string",
  "status": "enum: new | in_progress | done",
  "created_at": "ISO8601 datetime string"
}

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Купить молоко",
  "description": "Не забыть 2.5%",
  "status": "new",
  "created_at": "2026-09-17T09:50:00Z"
}