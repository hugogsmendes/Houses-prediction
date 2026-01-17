from fastapi import APIRouter, Depends
from utils.dependencies import get_user_adm, get_user_service
from schemas.user import UserDelete, UserSchemaDelete, UserSchemaResponse, UserCreate, UserAdminSchemaPost
from service.user_service import User_Service

adm_router = APIRouter(prefix="/api/v1/admin", tags=["admin"], dependencies=[Depends(get_user_adm)])

@adm_router.delete("/delete", status_code=200, response_model=UserDelete)
async def delete (user: UserSchemaDelete, service: User_Service = Depends(get_user_service)):
    return service.delete(user.username)

@adm_router.get("/list", status_code=200, response_model=list[UserSchemaResponse])
async def list_users (service: User_Service = Depends(get_user_service)):
    return service.list_all()

@adm_router.post("/create", status_code=201, response_model=UserCreate)
async def create_user (user_post: UserAdminSchemaPost, service: User_Service = Depends(get_user_service)):
    return service.create_user(user_post)