from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str

class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id:int
    items: list[Item] = []

    class Config:
        orm_mode = True

