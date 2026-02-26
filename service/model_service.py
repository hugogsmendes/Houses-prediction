from repository.model_repository import Model_Repository
import joblib
import os
from utils.exceptions import ModelUnavailable, Incompatibility
import pandas as pd
from schemas.model import ModelSchemaPost, PredictPriceResponse, PredictionResponse

def _format_brl(valor: float) -> str:
    # 1234.56 -> "1.234,56"
    s = f"{valor:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"

class Model_Service:


    def __init__(self, repository: Model_Repository):
        self.repository = repository

    def predict (self, data_predict: ModelSchemaPost, user_id: int) -> PredictPriceResponse:
        _data_predict = data_predict.model_dump() # transforma para dicionário
        try:
            x = pd.DataFrame([_data_predict])
            model_path = 'models_ml/model_mlp_v1.joblib'
            if not os.path.exists(model_path):
                raise ModelUnavailable
        except (ValueError, KeyError):
            raise Incompatibility
        
        model_svr = joblib.load(model_path)
        preco_previsto = float(model_svr.predict(x))

        self.create(_data_predict, preco_previsto, user_id)
        
        preco_previsto = _format_brl(preco_previsto)

        return PredictPriceResponse(preco_previsto=preco_previsto)
    
    def create (self, data_predict: dict, preco_previsto: float, user_id: int):

        _data_predict = data_predict.copy()
        _data_predict['preco_previsto'] = preco_previsto
        _data_predict['user_id'] = user_id
        return self.repository.create(_data_predict)
    
    def high_price (self) -> PredictionResponse:
        
        return self.repository.high_price()
