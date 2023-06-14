from fastapi import APIRouter

from app.routes import customer_routes

api_router = APIRouter()
api_router.include_router(customer_routes.router, tags=["customer"])


