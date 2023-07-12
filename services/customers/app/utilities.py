import sys
from typing import Dict, Any
from jose import jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from app.models import Users
from app.schemas import User, TokenPayload
from app.core.config import settings
from app.core import security
from app.database.database import get_db
from app.utils import users_crud

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)



def get_tracback() -> Dict[str, Any]:
    exc_type, exc_value, exc_tb = sys.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_string = str(exc_value)
    return {
        'error_type': str(exc_type),
        'line_number': line_number,
        'filename': filename,
        'error_string': error_string,
    }

def get_formatted_date(date):
    return f'{date.strftime(f"%d-%m-%Y")}'


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=get_tracback(),
        )
    user = users_crud.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user