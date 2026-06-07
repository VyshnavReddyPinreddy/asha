from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends,HTTPException,status 
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from core.config import settings 
import random 

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

bearer_scheme = HTTPBearer()

def verify_password(plain_password:str,hashed_password:str) -> bool : 
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict)->str : 
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def generate_otp()->str:
    return str(random.randint(100000,999999))

def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme),) -> dict : 
    token = credentials.credentials
    try : 
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms = [settings.JWT_ALGORITHM],
        )
        return payload 
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token",
            headers={"WWW-Authenticate":"Bearer"},
        )