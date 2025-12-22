from fastapi import Depends
from sqlalchemy.orm import Session
from database.session import SessionLocal
from repository.user_repository import User_Repository
from service.user_service import User_Service

def get_session ():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()

def get_user_repository (session: Session = Depends(get_session)):
    return User_Repository(session=session)

def get_user_service (repository: User_Repository = Depends(get_user_repository)):
    return User_Service(repository=repository)

