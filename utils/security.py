from passlib.context import CryptContext
import os
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM") 
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS= int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ouath2_schema = OAuth2PasswordBearer(tokenUrl="v1/user/login")

def hash_password(password:str):
    return bcrypt_context.hash(password)

def verify_password(password:str, hashed_password:str):
    return bcrypt_context.verify(password, hashed_password)

def create_access_token (username, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):

    expire_data = datetime.now(timezone.utc) + token_duration
    
    to_jwt = {
        "sub":str(username),
        "exp":expire_data,
        "type":"access"
    }

    encoded_jwt = jwt.encode(to_jwt,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token (username, token_duration=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)):
    
    expire_data = datetime.now(timezone.utc) + token_duration
    
    to_jwt = {
        "sub":str(username),
        "exp":expire_data,
        "type":"refresh"
    }

    encoded_jwt = jwt.encode(to_jwt,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_token (token:str):

    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

