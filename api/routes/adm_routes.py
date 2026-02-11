from fastapi import APIRouter, Depends, Request
from utils.dependencies import get_user_adm, get_user_service
from schemas.user import UserDelete, UserSchemaDelete, UserSchemaResponse, UserCreate, UserAdminSchemaPost
from service.user_service import User_Service
from main import limiter

adm_router = APIRouter(prefix="/v1/admin", tags=["admin"], dependencies=[Depends(get_user_adm)])

@adm_router.delete("/delete", status_code=200, response_model=UserDelete)
@limiter.limit("10/minute")
async def delete (request: Request, user: UserSchemaDelete, service: User_Service = Depends(get_user_service)):
    return service.delete(user.username)

@adm_router.get("/list", status_code=200, response_model=list[UserSchemaResponse])
@limiter.limit("10/minute")
async def list_users (request: Request, service: User_Service = Depends(get_user_service)):
    return service.list_all()

@adm_router.post("/create", status_code=201, response_model=UserCreate)
@limiter.limit("10/minute")
async def create_user (request: Request, user_post: UserAdminSchemaPost, service: User_Service = Depends(get_user_service)):
    return service.create_user(user_post)