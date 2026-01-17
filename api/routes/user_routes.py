from fastapi import APIRouter, Depends
from service.user_service import User_Service
from utils.dependencies import get_user_service, verify_refresh_token, get_user
from schemas.user import UserSchemaPost, UserCreate, UserLogin, RefreshToken, TokenJWT
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter(prefix="/api/v1", tags=["user"])

@user_router.post("/register", response_model=UserCreate, status_code=201)
async def create (user_post: UserSchemaPost, service: User_Service = Depends(get_user_service)):
    return service.create_user(user_post)

@user_router.post("/login", response_model=UserLogin, status_code=200)
async def login (user_login : OAuth2PasswordRequestForm = Depends(), service: User_Service = Depends(get_user_service)):
    return service.login(user_login)

@user_router.post("/refresh", response_model=TokenJWT, status_code=200)
async def refresh (token: RefreshToken, service: User_Service = Depends(get_user_service), 
                   current_user: dict = Depends(get_user)):
    username = verify_refresh_token(token, current_user)
    return service.get_refresh_token(username)