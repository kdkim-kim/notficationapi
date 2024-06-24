from datetime import datetime, timedelta, timezone
from typing import Annotated , Union
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # openssl rand -hex 32 시크릿 키
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 토큰 만료시간 30분

fake_user_db = { # 가상 유저 DB
    "kim": {
        "username": "kim",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "bC5oD@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    }
}

class Token(BaseModel): # 프론트엔드 유저의 토큰 값
    access_token: str # 보안토큰
    token_type: str # 토큰 타입

class TokenData(BaseModel): # 토큰이 가지고 있는 정보
    username : str | None = None

class User(BaseModel): #
    username : str
    email : Union[str, None] = None
    full_name : Union[str, None] = None
    disabled : Union[bool, None] = None

class UserInDB(User): # User 클래스 상속 하고 해시패스워드를 추가함
    hashed_password : str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # 보안 토큰

app = FastAPI()

def verify_password(plain_password, hashed_password): # 입력 패스워드와 디비에 해시된 패스워드 값 비교
    result = pwd_context.verify(plain_password, hashed_password)
    print(result, plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password) # 참 / 거짓 반환

def get_password_hash(password):
    return pwd_context.hash(password) # 패스워드 해시값 반환


def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db, username:str): # 유저가 DB 에 있으면 해시패스워드 반환
    if username in db: # 사용자명이 디비에 있으면
        user_dict = db[username] # 사용자 정보
        print(user_dict)
        return UserInDB(**user_dict) # 해시된 패스워드 정보를 포함 한 값 반환

def authenticate_user(fake_db, username: str, password: str): # 앤드프런트 입력데이타와 디비의 유져 자료 비교 검증
    user = get_user(fake_db, username) # 사용자명을 기준으로 데이타 조회 후 사용자의 해시된 패스워드 값을 포함함 노즌 정보 user에 할당
    if not user: # 사용자 명이 없으면
        return False
    if not verify_password(password, user.hashed_password): # 프런트앤드 입력 패스워드와 디비의 해시된 패스워드와 비교
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None): # 토큰 생성
    to_encode = data.copy()
    if expires_delta: # 로그인한 경우 (최초)
        expire = datetime.now(timezone.utc) + expires_delta # 현재에서 정한시간만큼 더함
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # 이미 로그인해서 사용 중인 경우 현재에서 15분 더함
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]): # 현재의 보안 토큰에서
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # 토큰이 가지고 있는 정보 값을 가져옴
        print(payload)
        username: str = payload.get("sub") #사용자 이름 값
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_user_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token: # 프론트 앤드 사용자 입력폼 데이타 토큰클래스로
    user  = authenticate_user(fake_user_db, form_data.username, form_data.password) # 사용자를 자료와 비교 검증하고 user[list]에 사용자 정보를 할당
    print(user)
    if not user: # 로그인 정보가 맞지 않을시
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # 토큰 유효시간
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires) # 토큰 생성
    result = Token(access_token=access_token, token_type="bearer")
    print(result)
    return Token(access_token=access_token, token_type = "bearer")

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
