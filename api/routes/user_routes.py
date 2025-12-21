from fastapi import APIRouter
from service.user_service import User_Service
from fastapi import Depends
from utils.dependencies import get_user_service
from schemas.user import UserSchemaPost

user_router = APIRouter(prefix="/v1/user", tags=["user"])

@user_router.post("/create", status_code=201)
async def create (user_create:UserSchemaPost,service: User_Service = Depends(get_user_service)):
    ...
