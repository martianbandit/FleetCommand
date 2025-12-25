from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import APP_NAME, DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES
    APP_NAME: str = APP_NAME
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
