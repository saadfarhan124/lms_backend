from app.models import Users, Permissions
from app.utils.base import CRUDBase
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserUpdate
from app.schemas import PermissionsCreate, PermissionsUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional, Union

class CRUDPermissions(CRUDBase[Permissions, PermissionsCreate, PermissionsUpdate]):
    pass

class CRUDUsers(CRUDBase[Users, UserCreate, UserUpdate]):

    def get_by_username(self, db: Session, *, username: str) -> Optional[Users]:
        return db.query(Users).filter(Users.user_name == username).first()

    def create_user(self, db: Session, user: UserCreate) -> Users:
        db_obj = Users(
            first_name=user.first_name,
            last_name=user.last_name,
            user_name=user.user_name,
            password=get_password_hash(user.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, username: str, password: str) -> Union[Optional[Users], int]:
        user = self.get_by_username(db, username=username)
        if not user:
            return 404
        if not verify_password(password, user.password):
            return 400
        return user

    def check_if_has_permission(self, db: Session, *, permission_int: int, db_obj: Users) -> bool:     
        if db_obj.is_super_user:
            return True   
        return any(permission_int == permission.permission_constant_id for permission in db_obj.permissions)

    def delete_user(self, db: Session, *, db_obj: Users) -> Users:
        permissions = [perm.id for perm in db_obj.permissions]
        db_obj.permissions.clear()    
        db.commit()
        db.query(Permissions).filter(Permissions.id.in_(permissions)).delete()
        db.delete(db_obj)
        db.commit()
        return db_obj

users_crud = CRUDUsers(Users)
permission_crud = CRUDPermissions(Permissions)