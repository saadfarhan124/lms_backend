from fastapi import APIRouter, Depends, HTTPException, status
from app.utils import users_crud, permission_crud
from app.utilities import get_tracback, get_current_user
from app.schemas import UserCreate, User, UsernameExists, UserList
from app.schemas import Login, LoginResponse, UpdatePassword
from app.schemas import PermissionsCreate, UserPermissionsUpdate
from app.constants import get_permission_strings, get_roles_strings
from app.constants import Permissions, role_permissions, is_valid_role, is_valid_permission, get_permission_string
from sqlalchemy.orm import Session
from app.database.database import get_db
from datetime import timedelta
from app.core.config import settings
from app.core import security
from typing import Any

router = APIRouter()


@router.post("/user", response_model=User)
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

@router.get("/users/{offset}/{limit}", response_model=UserList)
def get_users_by_pagination(offset: int, limit: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        users, count = users_crud.get_active_users(db, offset=offset, limit=limit, exclude_id=current_user.id)
        return UserList(users=users, count=count)
    except HTTPException as httpE:
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())
    
@router.get("/user/{id}", response_model=User)
def get_users_by_pagination(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return users_crud.get(db, id=id)
    except HTTPException as httpE:
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())
    

@router.delete("/user/{id}", response_model=User)
def delete_user_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        if not users_crud.check_if_has_permission(db, db_obj=current_user, permission_int=Permissions.ADD_USER.value):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized") 
        user_obj = users_crud.get(db, id=id)
        if user_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail= f"User with ID {id} does not exist")
        if user_obj.is_super_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete super user")
        
        return users_crud.delete_user(db, db_obj=user_obj)
    except HTTPException as httpE:
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())
    
@router.put("/update_permissions/{user_id}", response_model=User)
def update_permissions(user_id: int, permissions_request: UserPermissionsUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        if not users_crud.check_if_has_permission(db, db_obj=current_user, permission_int=Permissions.ADD_USER.value):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized") 
        else:
            user_obj = users_crud.get(db, id=user_id)
            if user_obj is None:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
            permissions = []
            if permissions_request.role_based:
                if not is_valid_role(permissions_request.permission_set):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Role")
                permissions = role_permissions[permissions_request.permission_set]
            else:
                permissions = permissions_request.permission_set
                if not all(is_valid_permission(perm) for perm in permissions):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Permission")
            permission_obj_list = []
            for perm in permissions:
                permission = PermissionsCreate(
                    permission_constant_id=perm,
                    title=get_permission_string(perm)
                )
                perm_obj = permission_crud.create(db, create_schema=permission)
                db.commit()
                db.refresh(perm_obj)
                permission_obj_list.append(perm_obj)
            return users_crud.update_permissions(db, db_obj=user_obj, permissions=permission_obj_list)
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

@router.put("/update_password/{user_id}", response_model=User)
def update_user_password(user_id: int, password: UpdatePassword, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        if not users_crud.check_if_has_permission(db, db_obj=current_user, permission_int=Permissions.ADD_USER.value):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
        else:
            user_obj = users_crud.get(db, id=user_id)
            return users_crud.update_password(db, db_obj=user_obj, password=password.password)
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
        if users_crud.check_if_has_permission(db, db_obj=current_user, permission_int=Permissions.ADD_USER.value):
            return True if users_crud.get_by_username(db, username=username.username) is not None else False
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    except HTTPException as httpE:
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=get_tracback())
