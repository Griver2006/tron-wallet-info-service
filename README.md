# Tron Wallet Info Microservice

Микросервис на FastAPI, который получает данные по адресу в сети Tron: `balance`, `bandwidth`, `energy`.

## Стек

- FastAPI  
- SQLAlchemy ORM (async)  
- TronPy  
- SQLite  
- Pytest (для тестов)

---

## Запуск проекта

### 1. Установить зависимости

```bash
pip install -r requirements.txt
```

> **Примечание:** убедитесь, что установлен Python 3.9+

### 2. Установить переменную окружения

Создайте `.env` файл или экспортируйте переменную вручную:

```env
API=your_trongrid_api_key
```

TronGrid API-ключ можно получить здесь: https://www.trongrid.io/

### 3. Запустить приложение

```bash
uvicorn app.main:app --reload
```

---

## Тесты

```bash
pytest
```

---

## Эндпоинты

### `POST /wallets`

Получить данные по адресу Tron-кошелька и сохранить в БД.

#### Пример запроса:

```json
{
  "address": "TXYZ1234567890"
}
```

#### Пример ответа:

```json
{
  "id": 1,
  "address": "TXYZ1234567890",
  "bandwidth": 500,
  "energy": 1500,
  "balance": 123.45,
  "created_at": "2025-04-03T12:00:00"
}
```

---

### `GET /wallets?skip=0&limit=10`

Получить список сохранённых запросов (с пагинацией).

#### Пример ответа:

```json
[
  {
    "id": 1,
    "address": "TXYZ1234567890",
    "bandwidth": 500,
    "energy": 1500,
    "balance": 123.45,
    "created_at": "2025-04-03T12:00:00"
  }
]
```

---

## Для разработки

### `POST /setup_datebase`

Этот эндпоинт пересоздаёт все таблицы в базе данных. Используется для отладки и тестирования.
