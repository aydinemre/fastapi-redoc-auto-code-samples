from typing import Optional

from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str

    class Config:
        schema_extra = {
            "example": {
                "title": "test-item"
            }
        }


# Properties to receive on item update
class ItemUpdate(ItemBase):
    class Config:
        schema_extra = {
            "example": {
                "title": "test-item",
                'description': "test-description"
            }
        }


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass