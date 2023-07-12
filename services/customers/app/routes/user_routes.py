from fastapi import APIRouter, Depends, HTTPException, status
from app.utils import users_crud
from app.utilities import get_tracback, get_current_user
from app.schemas import UserCreate, User
from app.schemas import Login, LoginResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from datetime import timedelta
from app.core.config import settings
from app.core import security
from typing import Any

router = APIRouter()


@router.post("/create_user", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return users_crud.create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())


@router.post("/login", response_model=LoginResponse)
def login(login: Login, db: Session = Depends(get_db)):
    response = users_crud.authenticate(
        db, username=login.user_name, password=login.password)
    if isinstance(response, int):
        if response == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")

    return LoginResponse(user=response, bearer_token=security.create_access_token(
        response.id, expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    ))

@router.post("/login/test-token", response_model=User)
def test_token(current_user: User = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user