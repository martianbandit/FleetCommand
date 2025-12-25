from pydantic_settings import BaseSettings

from app.core.constants import APP_NAME


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str = "change_me"
    APP_NAME: str = APP_NAME
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
