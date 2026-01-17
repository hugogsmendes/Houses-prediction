from models.users import User
from sqlalchemy import func
from utils.security import hash_password
from schemas.user import UserSchemaPost
class User_Repository:

    def __init__(self, session):
        self.session = session

    def find_by_username (self, username:str) -> User:
        return self.session.query(User).filter(func.lower(User.username) == func.lower(username)).first()
    
    def create (self, user_post:UserSchemaPost) -> User:
        new_user = User(username=user_post.username, password_hash=hash_password(user_post.password))
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
    def list_all (self):
        return self.session.query(User).all()
    
    def delete (self, user:User) -> None:
        self.session.delete(user)
        self.session.commit()