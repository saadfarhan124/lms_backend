from pydantic import BaseModel, validator, Field
from datetime import datetime
from typing import Optional, Union, List


class PermissionsCreate(BaseModel):
    permission_constant_id: int
    title: str


class PermissionsUpdate(PermissionsCreate):
    id: int


class Permissions(PermissionsUpdate):
    class Config:
        orm_mode = True

class Roles(BaseModel):
    id: int


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    role_based: bool = Field(exclude=True)
    permission_set: Union[List[int], int] = Field(exclude=True)
    password: str = Field(exclude=True)


class UserUpdate(UserCreate):
    id: int
    password: Optional[str] = Field(exclude=True)
    role_based: Optional[bool] = Field(exclude=True)
    permission_set: Optional[Union[List[int], int]] = Field(exclude=True)


class User(UserUpdate):
    role_based: Optional[bool] = Field(exclude=True)
    permission_set: Optional[Union[List[int], int]] = Field(exclude=True)
    time_created: datetime
    time_updated: datetime
    is_super_user: bool
    password: Optional[str] = Field(exclude=True)
    permissions: List[Permissions]

    class Config:
        orm_mode = True

class Login(BaseModel):
    user_name: str
    password: str


class LoginResponse(BaseModel):
    user: User = Field(exclude={'password'})
    bearer_token: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
