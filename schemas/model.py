from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field


BinaryFlag = Annotated[
    Literal[0, 1],
    Field(description="Variável binária: 0 = Não, 1 = Sim", examples=[0]),
]

class ModelSchemaPost (BaseModel):
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

    class Config:
        from_attributes = True

class PredictPriceResponse (BaseModel):

    preco_previsto: str

    class Config:
        from_attributes = True