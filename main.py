from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import settings

# 1. Импортируем ОБА роутера
from app.api.v1.api import api_router as api_router_v1
from app.api.v2.api import api_router_v2
from app.core.exceptions import InvalidFileTypeError
from fastapi.middleware.cors import CORSMiddleware
import logging



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


# Настройка базового конфига для логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"), # Запись в файл
        logging.StreamHandler()        # Вывод в консоль
    ]
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
