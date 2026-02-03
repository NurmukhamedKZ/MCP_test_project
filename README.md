Тестовое задание: AI Engineer разработчик - **AI-агент с MCP интеграцией для управления продуктами и заказами**

### Docker Compose

```bash
# 1. Клонируйте репозиторий
git clone <repo-url>
cd Test_task

# 2. Создайте .env файл с API ключом
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# 3. Запустите приложение
docker-compose up --build

# Или используйте Makefile
make build && make up
```

Приложение будет доступно на: **http://localhost:8000**

### Локально

```bash
# 1. Установите зависимости
pip install uv
uv pip install -r pyproject.toml

# 2. Создайте .env файл
echo "OPENAI_API_KEY=your_key" > .env

# 3. Запустите сервер
uvicorn app.fastapi_main:app --reload

---

## 📚 API Документация

### Endpoints

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Основные endpoints:

#### 1. `POST /api/v1/agent/query` - Запрос к агенту

```bash
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Покажи все продукты"}'
```

**Response:**
```json
{
  "result": "Вот список всех продуктов...",
  "status": "success",
  "error": null
}
```
---

### Структура тестов:

- `tests/test_api.py` - Тесты API endpoints (9 тестов)
- `tests/test_database.py` - Тесты базы данных (7 тестов)
- `tests/test_mcp_server.py` - Тесты MCP сервера (10 тестов)

**Всего: 26+ тестов** ✅

### Mock LLM для тестов:

Проект поддерживает работу **без реального OpenAI API ключа** для тестирования:

```python
# В .env укажите:
OPENAI_API_KEY=test-api-key

# Автоматически будет использован Mock LLM
```
---

## 📊 База данных

### Схема `products`:

| Колонка   | Тип     | Описание                    |
|-----------|---------|------------------------------|
| id        | INTEGER | Primary key (auto increment) |
| name      | TEXT    | Название продукта            |
| price     | REAL    | Цена                         |
| category  | TEXT    | Категория                    |
| in_stock  | INTEGER | В наличии (1/0)              |

### Схема `orders` (БОНУС):

| Колонка      | Тип     | Описание                     |
|--------------|---------|------------------------------|
| id           | INTEGER | Primary key (auto increment) |
| product_id   | INTEGER | ID продукта (FK)             |
| quantity     | INTEGER | Количество                   |
| total_price  | REAL    | Общая стоимость              |
| status       | TEXT    | Статус (pending/completed/cancelled) |
| created_at   | TEXT    | Дата создания (ISO)          |

---

## 🎯 MCP Серверы

### 1. Products Manager

**Tools:**
- `get_all_products()` - Получить список всех продуктов
- `get_product_by_id(product_id)` - Найти продукт по ID
- `add_new_product(name, price, category, in_stock)` - Добавить продукт
- `get_statistics()` - Статистика по продуктам

### 2. Orders Manager (БОНУС +10 баллов)

**Tools:**
- `create_order(product_id, quantity)` - Создать заказ
- `get_order(order_id)` - Получить заказ по ID
- `list_orders()` - Список всех заказов
- `update_order_status(order_id, status)` - Обновить статус
- `get_order_statistics()` - Статистика по заказам

---

## 🧮 Кастомные Tools (Калькулятор)

- `add(a, b)` - Сложение
- `subtract(a, b)` - Вычитание
- `multiply(a, b)` - Умножение
- `divide(a, b)` - Деление
- `power(base, exponent)` - Возведение в степень
- `calculate_percentage(total, percentage)` - Вычисление процента

---

## 📝 Логирование

Логи доступны:
- В stdout контейнера: `docker-compose logs -f`
- В файле: `app.log`
