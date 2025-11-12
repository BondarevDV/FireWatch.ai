# Расположение: /fire_detection_api/app/api/v1/api.py

from fastapi import APIRouter
from app.api.v1.endpoints import health, detect

# Главный роутер для версии v1
api_router = APIRouter()

# Подключаем роутер из health.py
api_router.include_router(health.router)
api_router.include_router(detect.router) 

# Сюда в будущем мы будем добавлять другие роутеры
# from app.api.v1.endpoints import users, items
# api_router.include_router(users.router)
# api_router.include_router(items.router)