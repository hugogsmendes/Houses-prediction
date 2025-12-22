from fastapi import Depends
from sqlalchemy.orm import Session
from database.session import SessionLocal
from repository.user_repository import User_Repository
from service.user_service import User_Service
from utils.security import ouath2_schema, verify_token
from utils.exceptions import Unauthorized

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

def get_user (token: str = Depends(ouath2_schema)):

    payload = verify_token(token)

    if not payload or payload.get("type") != "access":
        raise Unauthorized(detail="Token inválido ou expirado")
    
    username = payload.get("sub")
    if not username:
        raise Unauthorized(detail="Usuário inválido")
    
    return {
        "username": username
    }


