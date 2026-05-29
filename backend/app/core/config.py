from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    table_name: str = "ingredients"
    aws_default_region: str = "eu-central-1"
    aws_access_key_id: str = "local"
    aws_secret_access_key: str = "local"
    dynamodb_endpoint: str | None = None  # None = real AWS

    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()
