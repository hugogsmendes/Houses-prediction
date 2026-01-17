from repository.user_repository import User_Repository
from schemas.user import UserSchemaPost, UserSchemaResponse, UserSchemaLogin, UserLogin, UserAdminSchemaPost, UserCreate, TokenJWT
from utils.exceptions import RegisterExistsError, Unauthorized, RegisterNotFoundError
from utils.security import verify_password, create_access_token, create_refresh_token

class User_Service:

    def __init__(self, repository:User_Repository):
        self.repository = repository
    
    def create_user (self, user_post:UserSchemaPost | UserAdminSchemaPost) -> UserCreate:
        user = self.repository.find_by_username(user_post.username)

        if user:
            raise RegisterExistsError(register = f"Usuário {user.username}")
        is_admin = getattr(user_post, "is_admin", False) # acessa dinamicamente um valor de uma atributo de um objeto
        user_create = self.repository.create(user_post, is_admin)
        
        return{
            'message': 'Usuário criado com sucesso',
            'user': user_create
            }
    
    def login (self, user_login:UserSchemaLogin) -> UserLogin:

        user = self.repository.find_by_username(user_login.username)

        if not user or not verify_password(user_login.password, user.password_hash):
            raise Unauthorized(detail="Credencias inválidas")
        
        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)

        return {
            "message": "Login realizado com sucesso",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "user": user
        }

    def list_all (self) -> list[UserSchemaResponse]:
        return self.repository.list_all()
    
    def delete (self, username:str):

        user = self.repository.find_by_username(username)

        if not user:
            raise RegisterNotFoundError(register= f"Usuário {username}")
        
        self.repository.delete(user)

        return{
            "message": f"Usuário {username} deletado com sucesso"
        }
    
    def get_refresh_token (self, username: str) -> TokenJWT:

        access_token = create_access_token(username)
        refresh_token = create_refresh_token(username)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }


