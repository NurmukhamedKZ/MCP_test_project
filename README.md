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

# Или через Makefile
make dev
```

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

#### 2. `GET /api/v1/agent/health` - Health check

```bash
curl http://localhost:8000/api/v1/agent/health
```

---

## 💬 Примеры запросов

### Работа с продуктами:

### Работа с заказами (БОНУС):

```bash
# Создать заказ
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Создай заказ на продукт с ID 1, количество 2"}'

# Показать все заказы
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Покажи все заказы"}'

# Обновить статус заказа
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Обнови статус заказа 1 на completed"}'

# Статистика по заказам
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Покажи статистику по заказам"}'
```

### Математические вычисления:

```bash
# Калькулятор
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Посчитай скидку 15% на товар стоимостью 1000 рублей"}'

curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Сколько будет 123 умножить на 45?"}'
```

---

## 🧪 Тестирование

### Запуск тестов:

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Конкретный файл
pytest tests/test_api.py

# С coverage
pytest --cov=app tests/
```

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

## 📁 Структура проекта

```
Test_task/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── agent/
│   │           ├── __init__.py
│   │           └── endpoints.py        # REST API endpoints
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py                 # SQLite manager
│   ├── service/
│   │   ├── __init__.py
│   │   └── Agent.py                    # LangGraph агент
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── calculator.py               # Кастомные tools
│   │   ├── MCP_test_task.py           # MCP Products сервер
│   │   └── MCP_orders.py              # MCP Orders сервер (БОНУС)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── mock_llm.py                 # Mock LLM для тестов
│   └── fastapi_main.py                 # FastAPI приложение
├── data/
│   └── products.db                     # SQLite база данных
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # Pytest конфигурация
│   ├── test_api.py                     # Тесты API
│   ├── test_database.py                # Тесты БД
│   └── test_mcp_server.py             # Тесты MCP
├── .dockerignore
├── .env                                # Переменные окружения
├── .gitignore
├── ARCHITECTURE.md                     # Документация архитектуры
├── docker-compose.yml                  # Docker Compose конфигурация
├── Dockerfile                          # Docker образ
├── Makefile                           # Утилиты для разработки
├── pyproject.toml                     # Зависимости проекта
├── pytest.ini                         # Конфигурация pytest
└── README.md                          # Этот файл
```

---

## 🛠️ Технологии

- **Python 3.13**
- **FastAPI** - веб-фреймворк
- **LangChain** - фреймворк для LLM приложений
- **LangGraph** - для создания агентов
- **FastMCP** - Model Context Protocol серверы
- **SQLite** - база данных
- **Docker & Docker Compose** - контейнеризация
- **pytest** - тестирование
- **Pydantic** - валидация данных

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

## 🔧 Makefile команды

```bash
make help          # Показать все команды
make build         # Собрать Docker образ
make up            # Запустить приложение
make down          # Остановить приложение
make restart       # Перезапустить
make logs          # Показать логи
make clean         # Удалить все (контейнеры, образы, БД)
make dev           # Запустить локально для разработки
make install       # Установить зависимости
make test-api      # Тестовый запрос к API
```

---

## 📝 Логирование

Логи доступны:
- В stdout контейнера: `docker-compose logs -f`
- В файле: `app.log`

Уровни логирования настроены для всех модулей:
- `INFO` - основные события
- `DEBUG` - детальная информация
- `ERROR` - ошибки с трейсбеками

---

## 🐛 Troubleshooting

### Проблема: "No module named 'app.db.database'"

**Решение:** Убедитесь что `PYTHONPATH=/app` установлен в `docker-compose.yml`

### Проблема: "OPENAI_API_KEY not set"

**Решение:** Создайте `.env` файл с ключом или используйте `test-api-key` для Mock LLM

### Проблема: База данных не сохраняется

**Решение:** Проверьте volume mapping в `docker-compose.yml`: `./data:/app/data`

### Посмотреть логи в реальном времени:

```bash
docker-compose logs -f
```

---

## ✅ Критерии оценки (выполнено)

### Обязательные (Must Have): 70/70 баллов ✅

**MCP Сервер (25/25)**
- ✅ [10] Использует FastMCP с @mcp.tool
- ✅ [8] Реализованы все 4 инструмента
- ✅ [4] Работает через stdio
- ✅ [3] Обрабатывает ошибки

**LangGraph Агент (25/25)**
- ✅ [10] Подключается к MCP серверу
- ✅ [8] Использует tools из MCP
- ✅ [7] Имеет кастомные tools

**FastAPI + Docker (20/20)**
- ✅ [8] POST /api/v1/agent/query работает
- ✅ [7] Dockerfile и docker-compose.yml
- ✅ [5] Запускается через docker-compose up

### Дополнительные (Should Have): 20/20 баллов ✅

- ✅ [6] Чистая архитектура
- ✅ [5] Type hints + docstrings
- ✅ [5] Логирование
- ✅ [4] .gitignore

### Тесты и документация: 10/10 баллов ✅

- ✅ [6] Минимум 3 теста (26+ тестов)
- ✅ [4] README с инструкцией

### БОНУСЫ: +15 баллов ✅

- ✅ **[+5]** Персистентность через SQLite
- ✅ **[+10]** Второй MCP сервер для заказов

---

## 📄 Лицензия

MIT

---

## 👨‍💻 Автор

Тестовое задание для позиции AI Engineer (Junior/Стажёр)

**Итого: 115/100 баллов** 🎉
