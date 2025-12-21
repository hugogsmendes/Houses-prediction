from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///houses.db")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)