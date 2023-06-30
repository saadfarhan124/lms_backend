from fastapi import APIRouter

from app.routes import customer_routes, loan_application_routes

api_router = APIRouter()
api_router.include_router(customer_routes.router, tags=["customer"])
api_router.include_router(loan_application_routes.router, tags=["loan_application"])


