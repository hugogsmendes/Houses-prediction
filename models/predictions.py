from sqlalchemy import Column, Integer, ForeignKey, Float
from database.session import Base
from sqlalchemy.orm import Relationship

class Prediction (Base):
    __tablename__ = "predictions"

    id = Column("id", Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    area = Column("area", Float)
    quartos = Column("quartos", Integer)
    banheiros = Column("banheiros", Integer)
    andares = Column("andares", Integer)
    acesso_rodovia = Column("acesso_rodovia", Integer) # Variável binária
    quarto_hospede = Column("quarto_hospede", Integer) # Variável binária
    porao = Column("porao", Integer) # Variável binária
    aquecimento_agua = Column("aquecimento_agua", Integer) # Variável binária
    ar_condicionado = Column("ar_condicionado", Integer) # Variável binária
    vagas_estacionamento = Column("vagas_estacionamento", Integer)
    area_preferencial = Column("area_preferencial", Integer) # Variável binária
    status_mobilia_sem_mobilia = Column("status_mobilia_sem_mobilia", Integer) # Variável binária
    status_mobilia_semi_mobiliada = Column("status_mobilia_semi_mobiliada", Integer) # Variável binária
    preco_previsto = Column("preco_previsto", Float) # Preço previsto pelo modelo

    user = Relationship("User", back_populates="predictions", lazy="subquery")
