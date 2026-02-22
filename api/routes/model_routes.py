from fastapi import APIRouter, Depends, Request
from main import limiter
from utils.dependencies import get_model_service, get_user, get_user_service
from service.model_service import Model_Service
from service.user_service import User_Service
from schemas.model import ModelSchemaPost, PredictionResponse
import pandas as pd
from fastapi.responses import Response

model_route = APIRouter(prefix="/v1/model", tags=["model"])

@model_route.post("/predict", status_code=201)
@limiter.limit("10/minute")
async def predict (request: Request, data_predict: ModelSchemaPost, service: Model_Service = Depends(get_model_service),
                   current_user: dict = Depends(get_user), user_service: User_Service = Depends(get_user_service)):
    
    user_id = user_service.return_id_by_username(current_user.get("username"))
    return service.predict(data_predict, user_id)

@model_route.get("/high/price", status_code=200, response_model=PredictionResponse)
@limiter.limit("10/minute")
async def high_price (request: Request, service: Model_Service = Depends(get_model_service),
                      current_user: dict = Depends(get_user)):
    return service.high_price()

@limiter.limit("10/minute")
@model_route.get("/df", status_code = 200)
async def get_df (request: Request, current_user: dict = Depends(get_user)):
    df = pd.read_csv("models_ml/Housing_pre_processing.csv", sep = ",")
    csv_bytes = df.to_csv(index = False).encode("utf-8")

    return Response(
        content = csv_bytes,
        media_type = "text/csv",
        headers = {"Content-Disposition": 'attachment; filename="dataset.csv"'}
    )
