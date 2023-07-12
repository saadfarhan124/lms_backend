from pydantic import BaseModel, validator, Field
from datetime import datetime, date
from typing import Optional


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    password: str = Field(
        exclude=True
    )

class UserUpdate(UserCreate):
    id: int
    
class User(UserUpdate):
    time_created: datetime
    time_updated: datetime
    is_super_user: bool
    password: Optional[str] = None  # Override the password field
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