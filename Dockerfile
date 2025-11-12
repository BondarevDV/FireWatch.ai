# --- STAGE 1: Builder ---
# Устанавливает uv и собирает зависимости в "колеса"
FROM python:3.11-slim as builder

# 1. Устанавливаем сам uv
# uv написан на Rust и очень быстрый, но его нужно сначала установить.
RUN pip install uv

WORKDIR /app

# Копируем только файл с зависимостями для кэширования этого слоя
COPY requirements.txt .

# Создаем директорию для скомпилированных пакетов (wheels)
RUN mkdir /wheels

# 2. Используем uv для сборки "колес". Это будет значительно быстрее, чем pip.
# uv по умолчанию использует свою систему кэширования, так что --no-cache-dir не нужен.
RUN uv pip wheel --wheel-dir=/wheels -r requirements.txt

# --- STAGE 2: Runtime ---
# Создает финальный легковесный образ с приложением
FROM python:3.11-slim

# 3. Устанавливаем uv также и в финальном образе
RUN pip install uv

WORKDIR /app

# Копируем скомпилированные зависимости из builder-стадии
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .

# 4. Используем uv для установки зависимостей из локальных "колес".
# Это будет практически мгновенно и не требует доступа к сети.
RUN uv pip install --no-index --find-links=/wheels -r requirements.txt

# Копируем исходный код нашего приложения
COPY . .

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Команда для запуска. Для production можно заменить на запуск Gunicorn.
# Например: CMD ["/bin/bash", "scripts/run_prod.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]