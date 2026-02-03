# Используем официальный Python образ
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем uv для управления зависимостями
RUN pip install --no-cache-dir uv

# Устанавливаем зависимости проекта
RUN uv pip install --system --no-cache -r pyproject.toml

# Устанавливаем uvicorn для запуска FastAPI
RUN pip install --no-cache-dir uvicorn

# Копируем весь проект
COPY . .

# Создаем директорию для базы данных
RUN mkdir -p /app/app/db

# Открываем порт для FastAPI
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app.fastapi_main:app", "--host", "0.0.0.0", "--port", "8000"]
