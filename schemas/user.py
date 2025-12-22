from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserSchemaPost(BaseModel):

    username: str
    password: str
    is_activate: bool = True
    is_admin: bool = False

    class Config:
        from_attributes = True

class UserSchemaResponse (BaseModel):

    username: str
    is_activate: bool
    is_admin: bool
    create_at : date

    class Config:
        from_attributes = True

class UserSchemaLogin (BaseModel):

    username:str
    password:str

    class Config:
        from_attributes = True

