from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fire Detection API! 🔥"
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"

    # Определяет, какая версия API будет включена.
    # Возможные значения: "v1", "v2", "all"
    API_VERSION_TO_ENABLE: str = "v1"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()