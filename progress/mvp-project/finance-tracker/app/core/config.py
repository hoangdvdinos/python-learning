from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Finance Tracker API"
    APP_VERSION: str = "1.0.0"
    ENV: str = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:///./finance.db"

    model_config = {"env_file": ".env"}


settings = Settings()
