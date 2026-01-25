from repository.model_repository import Model_Repository
import joblib
import pandas as pd
from schemas.model import ModelSchemaPost, PredictPriceResponse

def _format_brl(valor: float) -> str:
    # 1234.56 -> "1.234,56"
    s = f"{valor:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"

class Model_Service:


    def __init__(self, repository: Model_Repository):
        self.repository = repository

    def predict (self, data_predict: ModelSchemaPost) -> PredictPriceResponse:
        _data_predict = data_predict.model_dump() # transforma para dicionário
        try:
            x = pd.DataFrame([_data_predict])
            x.rename(columns={"status_mobilia_sem-mobilia": "status_mobilia_sem-mobilia",
                              "status_mobilia_semi-mobiliada": "status_mobilia_semi-mobiliada"}, inplace=True)
            
            model_svr = joblib.load('models_ml/model_svr_v1.joblib')
            preco_previsto = model_svr.predict(x)
        except Exception as err:
            print(err)
        #self.create(data_predict, preco_previsto)
        return{
            "preco_previsto": f"{_format_brl(float(preco_previsto))}"
        }

    def create (self, data_predict: ModelSchemaPost, preco_previsto: float):
        ...