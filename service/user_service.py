from repository.user_repository import User_Repository
from schemas.user import UserSchemaPost, UserSchemaResponse
from utils.exceptions import RegisterExistsError

class User_Service:

    def __init__(self, repository:User_Repository):
        self.repository = repository
    
    def create_user (self, user_post:UserSchemaPost) -> UserSchemaResponse:
        user = self.repository.find_by_username(user_post.username)

        if user:
            raise RegisterExistsError(register = f"Usuário {user.username}")
        
        return self.repository.create(user_post)
