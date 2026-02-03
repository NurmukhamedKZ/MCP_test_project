# Test Task - Product Manager API

FastAPI приложение для управления продуктами с использованием SQLite и MCP серверов.

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLite** - база данных
- **LangChain** - интеграция с LLM
- **MCP (Model Context Protocol)** - инструменты для агента
- **Docker** - контейнеризация

## Быстрый старт с Docker

### 1. Создайте файл `.env` с вашим API ключом:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Запустите приложение:

**С Docker Compose:**
```bash
docker-compose up --build
```


Приложение будет доступно по адресу: http://localhost:8000

### 3. Документация API:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc




## Локальная разработка (без Docker)

### 1. Установите зависимости с помощью uv:

```bash
pip install uv
uv pip install -r pyproject.toml
pip install uvicorn
```

### 2. Создайте `.env` файл:

```bash
echo "OPENAI_API_KEY=your_key" > .env
```

### 3. Запустите сервер:

```bash
uvicorn app.fastapi_main:app --reload
```

## API Endpoints

### `GET /`
Информация о API

### `POST /ask_agent?prompt=ваш_запрос`
Отправить запрос агенту для работы с продуктами

**Примеры запросов:**
```bash
# Добавить продукт
curl -X POST "http://localhost:8000/ask_agent?prompt=добавь продукт iPhone 15 цена 999 категория Electronics в наличии"

# Получить все продукты
curl -X POST "http://localhost:8000/ask_agent?prompt=покажи все продукты"

# Статистика
curl -X POST "http://localhost:8000/ask_agent?prompt=покажи статистику по продуктам"
```

## Структура проекта

```
.
├── app/
│   ├── db/
│   │   └── database.py      # SQLite database manager
│   ├── service/
│   │   └── Agent.py         # LangChain agent
│   ├── tools/
│   │   ├── calculator.py    # Калькулятор инструменты
│   │   └── MCP_test_task.py # MCP сервер для продуктов
│   └── fastapi_main.py      # Главный файл приложения
├── data/                    # Папка для SQLite базы (создается автоматически)
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## База данных

База данных SQLite автоматически создается при первом запуске в папке `data/products.db`.

**Важно:**
- Класс `Database` находится в `app/db/database.py`
- MCP сервер импортирует его через `PYTHONPATH=/app`
- База данных монтируется как volume и сохраняется между перезапусками контейнера

### Схема таблицы `products`:

| Колонка   | Тип     | Описание                    |
|-----------|---------|------------------------------|
| id        | INTEGER | Primary key (auto increment) |
| name      | TEXT    | Название продукта            |
| price     | REAL    | Цена                         |
| category  | TEXT    | Категория                    |
| in_stock  | INTEGER | В наличии (1/0)              |
