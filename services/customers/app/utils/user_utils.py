from app.models import Users
from app.utils.base import CRUDBase
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional, Union


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


users_crud = CRUDUsers(Users)
