from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv

load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

                    # cria o BD e a engine para se conectar com ele
engine = create_engine(DATABASE_URL, pool_pre_ping = True, poolclass = NullPool)

Base = declarative_base() # declara um modelo padrão para usar nas entidades

SessionLocal = sessionmaker(bind=engine) # cria a sessão local com o BD