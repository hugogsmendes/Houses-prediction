from pydantic import BaseModel
from typing import Optional

class UserSchemaPost(BaseModel):

    username: str
    password:str
    is_activate: bool = True
    is_admin: bool = False

    class Config:
        from_attributes = True
