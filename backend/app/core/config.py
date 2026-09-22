from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ResearchOS API"
    environment: str = Field(
        default="development",
        validation_alias="APP_ENV",
    )
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./researchos.db"


settings = Settings()

