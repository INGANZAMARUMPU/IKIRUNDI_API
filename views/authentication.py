from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from database import schemas, instance


router = APIRouter()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "2c687097f08297c0513ccecacadc90c3d2b02d97356e02cab61523786d878d58"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 24*14

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verifyPassword(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticateUser(username: str, password: str):
    result = instance.getBucket("users").get(username, quiet=True)
    if not result.value:
        return False
    user = schemas.User(**result.value)
    if not verifyPassword(password, user.password):
        return False
    return user

def createAccessToken(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode.update({"token_type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def createRefreshToken(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    to_encode.update({"token_type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login_required(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expire: int = payload.get("exp")
        token_type: str = payload.get("token_type")
        is_expired: bool = expire < datetime.utcnow().timestamp()
        if username is None or is_expired or token_type != "access":
            raise CREDENTIALS_EXCEPTION
        return token
    except: #jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError:
        raise CREDENTIALS_EXCEPTION

# async def getTokenUser(db: Session = Depends(get_db),token:str = Depends(login_required)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     user = await getUser(username=payload.get("sub"), db=db)
#     if user is None:
#         raise CREDENTIALS_EXCEPTION
#     return user

# async def getRefreshUser(db: Session, refresh:str = Depends(login_required)):
#     try:
#         payload = jwt.decode(refresh, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         expire: int = payload.get("exp")
#         token_type: str = payload.get("token_type")
#         is_expired: bool = expire < datetime.utcnow().timestamp()
#         if username is None or is_expired or token_type != "refresh":
#             raise CREDENTIALS_EXCEPTION
#     except: #jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError:
#         raise CREDENTIALS_EXCEPTION
#     user = await getUser(username, db)
#     if user is None:
#         raise CREDENTIALS_EXCEPTION
#     return user

@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticateUser(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Doesn't exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = createAccessToken(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = createRefreshToken(
        data={"sub": user.email},
        expires_delta=timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "username":user.email,
        "role":user.role
    }

# @router.post("/refresh/{refresh}", response_model=schemas.RefreshedToken)
# async def refreshToken(refresh: str = Depends(get_db)):
#     user = await getRefreshUser(db, refresh)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = createAccessToken(
#         data={"sub": user.email},
#         expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     return {
#         "access_token": access_token,
#         "token_type": "bearer"
#     }