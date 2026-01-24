from pydantic import BaseModel

class ModelSchemaPost (BaseModel):
    area: float
    quartos: int
    banheiros: int
    andares: int
    acesso_rodovia: int
    quarto_hospede: int
    porao: int
    aquecimento_agua: int
    ar_condicionado: int
    vagas_estacionamento: int
    area_preferencial: int
    status_mobilia_sem_mobilia: int
    status_mobilia_semi_mobiliada: int
    class config:
        from_attributes = True

class PredictPriceResponse (BaseModel):

    preco_previsto: str

    class config:
        from_attributes = True