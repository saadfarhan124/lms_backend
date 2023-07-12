from fastapi import APIRouter, Depends, HTTPException, status
from app.utils import users_crud, permission_crud
from app.utilities import get_tracback, get_current_user
from app.schemas import UserCreate, User, UsernameExists
from app.schemas import Login, LoginResponse
from app.schemas import PermissionsCreate
from app.constants import get_permission_strings, get_roles_strings
from app.constants import Permissions, role_permissions, is_valid_role, is_valid_permission, get_permission_string
from sqlalchemy.orm import Session
from app.database.database import get_db
from datetime import timedelta
from app.core.config import settings
from app.core import security
from typing import Any

router = APIRouter()


@router.post("/create_user", response_model=User)
def create_user(user: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
    try:
        if not users_crud.check_if_has_permission(db, db_obj=current_user, permission_int=Permissions.ADD_USER.value):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        else:
            user_obj = users_crud.create_user(db, user)
            permissions = []
            if user.role_based:
                if not is_valid_role(user.permission_set):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Role")
                permissions = role_permissions[user.permission_set]
            else:
                permissions = user.permission_set
                if not all(is_valid_permission(perm) for perm in permissions):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Permission")
            for perm in permissions:
                permission = PermissionsCreate(
                    permission_constant_id=perm,
                    title=get_permission_string(perm)
                )
                perm_obj = permission_crud.create(db, create_schema=permission)
                user_obj.permissions.append(perm_obj)
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
            return user_obj
    except HTTPException as httpE:
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())


@router.post("/login", response_model=LoginResponse)
def login(login: Login, db: Session = Depends(get_db)):
    try:
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
    except HTTPException as httpE:
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())


@router.post("/login/test-token", response_model=User)
def test_token(current_user: User = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


# Utils
@router.get("/permissions")
def permissions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Any:
    try:
        print(role_permissions)
        if users_crud.check_if_has_permission(db, db_obj=current_user, permission_int=Permissions.ADD_USER.value):
            return get_permission_strings()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    except HTTPException as httpE:
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())


@router.get("/roles")
def roles(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Any:
    try:
        if users_crud.check_if_has_permission(db, db_obj=current_user, permission_int=Permissions.ADD_USER.value):
            return get_roles_strings()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    except HTTPException as httpE:
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())


@router.get("/check_username")
def check_username_if_exists(username: UsernameExists, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> bool:
    try:
        return True if users_crud.get_by_username(db, username=username.username) is not None else False
    except HTTPException as httpE:
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())
