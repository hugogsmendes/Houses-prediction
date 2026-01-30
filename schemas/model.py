from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field


BinaryFlag = Annotated[
    Literal[0, 1],
    Field(description="Variável binária: 0 = Não, 1 = Sim", examples=[0]),
]

class ModelSchemaPost (BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    area: float
    quartos: int
    banheiros: int
    andares: int
    acesso_rodovia: BinaryFlag
    quarto_hospede: BinaryFlag
    porao: BinaryFlag
    aquecimento_agua: BinaryFlag
    ar_condicionado: BinaryFlag
    vagas_estacionamento: int
    area_preferencial: BinaryFlag
    status_mobilia_sem_mobilia: BinaryFlag
    status_mobilia_semi_mobiliada: BinaryFlag


class PredictPriceResponse (BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    preco_previsto: str

class PredictionResponse (BaseModel):

    model_config = ConfigDict(from_attributes=True)

    quartos: int
    acesso_rodovia: int
    porao: int
    aquecimento_agua: int
    vagas_estacionamento: int
    status_mobilia_sem_mobilia: int
    status_mobilia_semi_mobiliada: int
    area: float
    banheiros: int
    andares: int
    quarto_hospede: int
    ar_condicionado: int
    area_preferencial: int
    preco_previsto: float

