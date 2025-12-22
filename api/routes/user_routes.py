from fastapi import APIRouter, Depends
from service.user_service import User_Service
from utils.dependencies import get_user_service
from schemas.user import UserSchemaPost, UserSchemaResponse

user_router = APIRouter(prefix="/v1/user", tags=["user"])

@user_router.post("/create", response_model=UserSchemaResponse, status_code=201)
async def create (user_post: UserSchemaPost,service: User_Service = Depends(get_user_service)):
    return service.create_user(user_post)
