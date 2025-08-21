from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Auth Example"
    secret_key: str = "supersecretkey"
    debug: bool = True


settings = Settings()
