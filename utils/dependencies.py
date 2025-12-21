from fastapi import Depends
from database.session import SessionLocal

def get_session ():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()