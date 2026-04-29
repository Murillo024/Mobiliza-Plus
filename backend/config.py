from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "mobiliza"
    CORS_ORIGIN: str = "http://localhost:4200"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
