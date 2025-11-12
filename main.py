from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.logging_config import setup_logging
from app.core.config import settings

# 1. Импортируем ОБА роутера
from app.api.v1.api import api_router as api_router_v1
from app.api.v2.api import api_router_v2
from app.core.exceptions import InvalidFileTypeError
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

# 2. ВЫЗЫВАЕМ ФУНКЦИЮ НАСТРОЙКИ ЛОГИРОВАНИЯ
# Это нужно сделать в самом начале, до создания экземпляра FastAPI
setup_logging()

# Создаем экземпляр логгера для использования в этом файле
logger = logging.getLogger(__name__)

# Настройка CORS
origins = [
    "http://localhost",
    "http://localhost:3000", # Для React/Vue/Angular разработки
    "http://localhost:8080",
    # "https://your-production-frontend.com" # Домен твоего фронтенда в продакшене
]

app = FastAPI(
    title=settings.PROJECT_NAME,
)




app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Разрешить все методы (GET, POST, etc.)
    allow_headers=["*"], # Разрешить все заголовки
)


@app.exception_handler(InvalidFileTypeError)
async def invalid_file_type_exception_handler(request: Request, exc: InvalidFileTypeError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )

@app.get("/")
def read_root():
    """
    Корневой эндпоинт.
    """
    return {"message": f"Welcome! Active API version(s) controlled by env: '{settings.API_VERSION_TO_ENABLE}'"}

@app.get("/test-error", summary="Вызвать тестовую ошибку")
def trigger_error():
    """
    Этот эндпоинт специально создан для проверки системы логирования.
    Он вызывает ошибку деления на ноль, перехватывает ее и логирует.
    """
    logger.info("Получен запрос на эндпоинт /test-error")
    try:
        # Вызываем ошибку
        x = 1 / 0
    except ZeroDivisionError:
        # Логируем ее с полной информацией о трассировке
        logger.error(
            "Тестовая ошибка! Деление на ноль было успешно перехвачено.", 
            exc_info=True
        )
        # Пользователю не нужно видеть страшный traceback,
        # поэтому возвращаем адекватное сообщение.
        # Вся "грязь" останется в логах для разработчика.
        return {
            "status": "error",
            "message": "Внутренняя ошибка сервера была залогирована."
        }

@app.get("/test-warning", summary="Вызвать тестовое предупреждение")
def trigger_warning():
    """
    Этот эндпоинт проверяет наличие необязательной переменной окружения.
    Если ее нет, он логирует предупреждение и продолжает работу.
    """
    logger.info("Получен запрос на эндпоинт /test-warning")
    
    # Проверяем, установлена ли переменная окружения LEGACY_MODE
    # os.getenv вернет None, если переменной нет
    if os.getenv("LEGACY_MODE") is None:
        # Это идеальный случай для WARNING: приложение работает, но мы хотим
        # сообщить разработчику, что используется режим по умолчанию.
        logger.warning(
            "Переменная окружения 'LEGACY_MODE' не установлена. "
            "Используется стандартный режим работы."
        )
        return {
            "status": "ok",
            "mode": "standard",
            "message": "Предупреждение было залогировано."
        }
    else:
        logger.info("Приложение работает в LEGACY_MODE.")
        return {
            "status": "ok",
            "mode": "legacy",
            "message": "Предупреждение не требуется."
        }

# 2. Добавляем логику условного подключения роутеров
if settings.API_VERSION_TO_ENABLE == "v1":
    print("INFO:     Enabling API v1")
    app.include_router(api_router_v1, prefix=settings.API_V1_STR)

elif settings.API_VERSION_TO_ENABLE == "v2":
    print("INFO:     Enabling API v2")
    app.include_router(api_router_v2, prefix=settings.API_V2_STR)

elif settings.API_VERSION_TO_ENABLE == "all":
    print("INFO:     Enabling all API versions (v1 and v2)")
    app.include_router(api_router_v1, prefix=settings.API_V1_STR)
    app.include_router(api_router_v2, prefix=settings.API_V2_STR)
else:
    # Если в .env указано что-то не то, лучше упасть с ошибкой при старте
    raise ValueError("Invalid value for API_VERSION_TO_ENABLE. Use 'v1', 'v2', or 'all'.")
