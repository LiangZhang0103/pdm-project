from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://pdm:pdm123@localhost:5432/pdm"
    database_test_url: str = "postgresql://pdm:pdm123@localhost:5432/pdm_test"

    # MinIO (S3 compatible storage)
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "pdm"
    minio_secret_key: str = "pdm123"
    minio_bucket: str = "pdm-documents"
    minio_secure: bool = False

    # JWT Authentication
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    # Application
    environment: str = "development"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # AI Services
    enable_ai_features: bool = True
    ocr_language: str = "ch"
    embedding_model: str = "all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"


settings = Settings()
