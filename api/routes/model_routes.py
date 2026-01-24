from fastapi import APIRouter, Depends, Request
from main import limiter
from utils.dependencies import get_model_service, get_user
from service.model_service import Model_Service
from schemas.model import ModelSchemaPost

model_route = APIRouter(prefix="/api/v1/model", tags=["model"])

@model_route.post("/predict", status_code=201)
@limiter.limit("10/minute")
async def predict (request: Request, data_predict: ModelSchemaPost, service: Model_Service = Depends(get_model_service),
                   current_user: dict = Depends(get_user)):
    
    return service.predict(data_predict)