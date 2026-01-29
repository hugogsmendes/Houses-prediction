from pydantic import BaseModel, ConfigDict
from datetime import date

class UserSchemaPost(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str


class UserAdminSchemaPost(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str
    is_admin: bool = False


class UserSchemaResponse (BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username: str
    is_activate: bool
    is_admin: bool
    create_at : date


class UserSchemaLogin (BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username:str
    password:str

class UserCreate (BaseModel):

    model_config = ConfigDict(from_attributes=True)

    message: str
    user: UserSchemaResponse
    

class UserLogin (BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    message: str
    access_token: str
    refresh_token: str
    token_type: str
    user: UserSchemaResponse


class UserSchemaDelete (BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username: str


class UserDelete (BaseModel):

    model_config = ConfigDict(from_attributes=True)

    message: str


class RefreshToken (BaseModel):

    model_config = ConfigDict(from_attributes=True)

    refresh_token:str


class TokenJWT (BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    token_type: str
