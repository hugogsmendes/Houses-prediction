from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
                    # cria o BD e a engine para se conectar com ele
engine = create_engine(DATABASE_URL, pool_pre_ping = True)

Base = declarative_base() # declara um modelo padrão para usar nas entidades

SessionLocal = sessionmaker(bind=engine) # cria a sessão local com o BD