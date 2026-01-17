from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserSchemaPost(BaseModel):

    username: str
    password: str
    class Config:
        from_attributes = True

class UserAdminSchemaPost(BaseModel):

    username: str
    password: str
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
class UserCreate (BaseModel):

    message: str
    user: UserSchemaResponse
    class Config:
        from_attributes = True

class UserLogin (BaseModel):
    
    message: str
    access_token: str
    refresh_token: str
    token_type: str
    user: UserSchemaResponse
    class Config:
        from_attributes = True

class UserSchemaDelete (BaseModel):

    username: str
    class Config:
        from_attributes = True

class UserDelete (BaseModel):

    message: str

    class Config:
        from_attributes = True

class RefreshToken (BaseModel):

    refresh_token:str

    class Config:
        from_attributes = True

class TokenJWT (BaseModel):

    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True