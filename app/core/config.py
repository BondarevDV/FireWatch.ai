from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
        Класс для хранения всех настроек приложения.
        Pydantic автоматически читает переменные из .env файла.
    """
    PROJECT_NAME: str = "Fire Detection API! 🔥"
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"
    # Уровень логирования. По умолчанию 'INFO', если не задан в .env
    LOG_LEVEL: str = "INFO"
    
    # Здесь можно добавлять другие настройки в будущем, например:
    # DATABASE_URL: str
    # RABBITMQ_URL: str
    # Определяет, какая версия API будет включена.
    # Возможные значения: "v1", "v2", "all"
    API_VERSION_TO_ENABLE: str = "v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True # Например, если переменные в .env могут быть в разном регистре
    )

settings = Settings()