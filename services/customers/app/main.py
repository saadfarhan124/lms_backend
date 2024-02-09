from fastapi import FastAPI
# from app.database.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware


from app.core.config import settings
# from app.routes.api import api_router

# import app.models

# from .routes import example_routes

# Base.metadata.create_all(bind= engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
# app.include_router(api_router, prefix=settings.API_V1_STR)

 