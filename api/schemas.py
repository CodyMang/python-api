from pydantic import BaseModel, HttpUrl


class ItemBase(BaseModel):
    description: str


class ItemCreate(ItemBase):
    pass


class ItemURL(BaseModel):
    content: HttpUrl
    class Config:
        orm_mode = True
    

class Item(ItemBase):
    id: int
    owner_id: int
    item_urls: list[ItemURL]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
