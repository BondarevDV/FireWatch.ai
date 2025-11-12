from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health_v2"]) # <-- Изменим тег для наглядности
def health_check_v2():
    """
    Проверяет, работает ли сервис (Версия 2).
    """
    return {"status": "ok", "version": "v2"} # <-- Добавим версию в ответ