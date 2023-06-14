from fastapi import FastAPI
from app.database.database import engine, Base

from app.core.config import settings
from app.routes.api import api_router

from app.models import Customer

# from .routes import example_routes

Base.metadata.create_all(bind= engine)

app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(api_router, prefix=settings.API_V1_STR)

