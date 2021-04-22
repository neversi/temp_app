from logging import disable
from request import make_request
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from .main import app, redis_cache

from .config import Config
from .exceptions import UserNotExist

ACCESS_SECRET_KEY = Config.ACCESS_SECRET_KEY
REFRESH_SECRET_KEY = Config.REFRESH_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshToken(BaseModel):
        refresh_token: str
        token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class User(BaseModel):
        email: str
        disabled: Optional[bool] = None

class UserIn(User):
        hash_password: str

# async def create_auth(user_id: int, token_uuid: str):
        # pass

def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(email: str) -> Optional[UserIn]:
        response = await make_request(Config.STUDENT_SERVICE_URL + "/students/" + email, "get")
        if "email" not in response[0]:
                return None
        return UserIn(**response[0].dict())

async def authenticate_user(email: str, password: str):
        user = await get_user(email)
        if not user:
                return False
        if not verify_password(password, user.hash_password):
                return False

def create_token(data: dict, secret: str, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
                expire = datetime.utcnow() + expires_delta
        else: 
                expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret, algorithm=ALGORITHM)
        return encoded_jwt

async def get_current_user(secret: str, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(email=email)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = await get_user(email=token_data.email)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=7)
    access_token = create_token(data={"sub": form_data.email}, secret = ACCESS_SECRET_KEY, expires_delta=access_token_expires)
    refresh_token = create_token(data={"sub": form_data.email}, secret = REFRESH_SECRET_KEY, expires_delta=refresh_token_expires)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/refresh", response_model=Token)
async def refresh(token: str = Depends(oauth2_scheme)):
        try:
                payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
                email: str = payload.get("sub")
                if email is None:
                        raise CREDENTIALS_EXCEPTION
                token_data = TokenData(email=email)
        except JWTError:
                raise CREDENTIALS_EXCEPTION
        user = await get_user(email=token_data.email)
        if user is None:
                raise CREDENTIALS_EXCEPTION
        access_token_expires =  timedelta (minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta (days=7)
        access_token = create_token(data={"sub": token_data.email}, secret = ACCESS_SECRET_KEY, expires_delta=access_token_expires)
        refresh_token = create_token(data={"sub": token_data.email}, secret = REFRESH_SECRET_KEY, expires_delta=refresh_token_expires)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}