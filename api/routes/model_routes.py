from fastapi import APIRouter, Depends, Request
from main import limiter
from utils.dependencies import get_model_service, get_user
from service.model_service import Model_Service

model_route = APIRouter(prefix="/api/v1/model", tags=["model"], dependencies=[Depends(get_user)])

@model_route.post("/predict", status_code=201)
@limiter.limit("10/minute")
async def predict (request: Request, service: Model_Service = Depends(get_model_service)):
    ...