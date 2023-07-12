from pydantic import BaseSettings
import os, secrets

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.getenv('SQLALCHEMY_DATABASE_URI')

    # SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:postgres@lmsdb:5432/lms_db"
    PROJECT_NAME = "Bravos_LMS"
    API_V1_STR = "/api/v1"
    SECRET_KEY: str = "sadFrhn12"
    
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8



settings = Settings()