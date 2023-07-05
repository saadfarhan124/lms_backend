from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.getenv('SQLALCHEMY_DATABASE_URI')

    # SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:postgres@lmsdb:5432/lms_db"
    PROJECT_NAME = "Bravos_LMS"
    API_V1_STR = "/api/v1"

settings = Settings()