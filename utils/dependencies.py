from fastapi import Depends
from sqlalchemy.orm import Session
from database.session import SessionLocal
from repository.user_repository import User_Repository
from service.user_service import User_Service
from utils.security import ouath2_schema, verify_token
from utils.exceptions import Unauthorized, NotPermission
from schemas.user import RefreshToken

def get_session (): # Pega a sessão do BD
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()

def get_user_repository (session: Session = Depends(get_session)): # Injeta a session em repository para que ele faça operações no BD
    return User_Repository(session=session)

def get_user_service (repository: User_Repository = Depends(get_user_repository)): # Injeta o repository em service para que o service use a camada repository
    return User_Service(repository=repository)

def get_user (token: str = Depends(ouath2_schema)): # FastAPI pega o token do header e injeta ele na função

    payload = verify_token(token)

    if not payload or payload.get("type") != "access": # Se não for um paypload válido ou que não seja tipo "access"
        raise Unauthorized(detail="Token inválido ou expirado")
    
    username = payload.get("sub")
    if not username:
        raise Unauthorized(detail="Usuário inválido")
    
    return {
        "username": username
    }

def get_user_adm (current_user: dict = Depends(get_user), user_service: User_Service = Depends(get_user_service)):

    user = user_service.repository.find_by_username(current_user.get("username"))

    if not user.is_admin:
        raise NotPermission
    
    return

def verify_refresh_token (token: RefreshToken, current_user:dict):
    
    payload = verify_token(token.refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise Unauthorized(detail="Token inválido ou expirado")
    
    username = payload.get("sub")
    current_username = current_user.get("username")
    if username != current_username:
        raise Unauthorized(detail="Usuário inválido")
    
    return username