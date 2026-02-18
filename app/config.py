from pydantic_settings import BaseSettings


# Application settings loaded from environment variables
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    DEBUG: bool = False
    APP_TITLE: str = "CRUD API"
    APP_VERSION: str = "1.0.0"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
