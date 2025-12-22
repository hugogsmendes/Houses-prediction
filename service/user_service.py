from repository.user_repository import User_Repository
from schemas.user import UserSchemaPost, UserSchemaResponse, UserSchemaLogin
from utils.exceptions import RegisterExistsError, Unauthorized
from utils.security import verify_password, create_access_token, create_refresh_token

class User_Service:

    def __init__(self, repository:User_Repository):
        self.repository = repository
    
    def create_user (self, user_post:UserSchemaPost) -> UserSchemaResponse:
        user = self.repository.find_by_username(user_post.username)

        if user:
            raise RegisterExistsError(register = f"Usuário {user.username}")
        
        return self.repository.create(user_post)
    
    def login (self, user_login:UserSchemaLogin):

        user = self.repository.find_by_username(user_login.username)

        if not user or not verify_password(user_login.password, user.password_hash):
            raise Unauthorized(detail="Credencias inválidas")
        
        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }


