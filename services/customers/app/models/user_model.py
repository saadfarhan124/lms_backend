from app.database.database import Base
from sqlalchemy import Column, String, DateTime, Date, Integer, Date, DECIMAL, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


user_permissions = Table('user_permissions', Base.metadata,
                                    Column('user_id', Integer,
                                           ForeignKey('users.id')),
                                    Column('permission_id', Integer,
                                           ForeignKey('permissions.id'))
                                    )

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    user_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_super_user = Column(Boolean, default=False, nullable=False)
    permissions = relationship(
        "Permissions", secondary=user_permissions, back_populates="users")
    time_created = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Permissions(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    users = relationship(
        "Users", secondary=user_permissions, back_populates="permissions")