from fastapi import APIRouter, Depends
from service.user_service import User_Service
from utils.dependencies import get_user_service, get_user, get_user_adm
from schemas.user import UserSchemaPost, UserCreate, UserSchemaResponse, UserLogin, UserSchemaDelete, UserDelete
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter(prefix="/api/v1", tags=["user"])

@user_router.post("/register", response_model=UserCreate, status_code=201)
async def create (user_post: UserSchemaPost, service: User_Service = Depends(get_user_service)):
    return service.create_user(user_post)

@user_router.post("/login", response_model=UserLogin, status_code=200)
async def login (user_login : OAuth2PasswordRequestForm = Depends(), service: User_Service = Depends(get_user_service)):
    return service.login(user_login)

@user_router.get("/list", status_code=200, response_model=list[UserSchemaResponse])
async def list_users (service: User_Service = Depends(get_user_service), current_user: dict = Depends(get_user)):
    return service.list_all()

@user_router.delete("/delete", status_code=200, response_model=UserDelete)
async def delete (user: UserSchemaDelete, service: User_Service = Depends(get_user_service), 
                current_user: dict = Depends(get_user_adm)):
    return service.delete(user.username)