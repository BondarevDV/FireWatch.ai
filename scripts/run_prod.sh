#!/bin/bash

# Количество воркеров. Хорошее правило: (2 * кол-во ядер CPU) + 1
WORKERS=${WORKERS:-4}

# Запуск Gunicorn с воркерами Uvicorn
# --bind 0.0.0.0:8000 - слушать на всех сетевых интерфейсах на порту 8000
# -k uvicorn.workers.UvicornWorker - использовать Uvicorn для обработки запросов
gunicorn main:app --workers $WORKERS --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000