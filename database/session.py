from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///houses.db") # cria o BD e a engine para se conectar com ele

Base = declarative_base() # declara um modelo padrão para usar nas entidades

SessionLocal = sessionmaker(bind=engine) # cria a sessão local com o BD