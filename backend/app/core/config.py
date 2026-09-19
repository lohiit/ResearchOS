from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ResearchOS API"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./researchos.db"


settings = Settings()
