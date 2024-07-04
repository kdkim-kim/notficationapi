from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.security import APIKeyHeader
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from passlib.context import CryptContext

from app.config.excuteSL import ( userAPIkey, userPasschk, cre_pass, userPassAtuth, create_tables, getSubclass, getSource,
    getTags, get_widget_tag, getSubclassit )
from app.config.schema import passNum

app = FastAPI() # FASTAPI

API_KEY = None # 보안 키
API_KEY_NAME = "access-token" # 키 이름
USER = None # 사용자명
USER_KEY_NAME ="users" # 사용자명 이름
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False) # KEY HEADER
username = APIKeyHeader(name=USER_KEY_NAME, auto_error=False) # USER HEADER

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #

def in_apikey(api_key_: str): # api_key 원본값
    return api_key_.split(" ")[0]

def get_pass_hash(password): # 패스워드 해시 값 반환
    return bcrypt_context.hash(password)
def verify_password(plain_password, hashed_password): # 입력 패스워드와 디비에 해시된 패스워드 값 비교
    result = bcrypt_context.verify(plain_password, hashed_password)
    return result  # 참 / 거짓 반환


async def get_api_key(api_key_: str = Depends(api_key_header), username: str = Depends(username)): # 사용자와 클라이언트 키값 비교
    #api_key_var_ = in_apikey(api_key_) # DB 자료 비교용 키값
    #print(api_key_var_)
    result = userAPIkey(username, in_apikey(api_key_)) # 관리자로 부터 할당 받은 사용자명과 보안키 값 검증
    if result:
        global API_KEY, USER
        API_KEY = api_key_ # 보안키 값을 전역변수에 할당
        USER = username
        print(API_KEY, USER)
        return
    else:
        raise HTTPException(status_code=400, detail="Not valid")

async def get_active_auth(api_key: str = Depends(api_key_header)): # 접속시 할당 받은 키 값과 접속프로그램의 키캆 비교
    global API_KEY, USER
    #print(api_key, API_KEY)
    if API_KEY == api_key:
        return
    else:
        API_KEY = None
        USER = None
        raise HTTPException(status_code=400, detail="Not valid")

@app.get("/connect/") # @app 최초접속 USER와 KEY 값 검증
async def connect(api_key: str = Depends(get_api_key), username: str= Depends(username)):
    result = userPasschk(USER, in_apikey(API_KEY))
    create_tables()
    return {result}

@app.post("/app/crePass/", dependencies=[Depends(get_active_auth)]) # @app 패스워드 생성
async def create_pass(pass_num: passNum):
    hashed_pass0 = get_pass_hash(pass_num.pass0)
    hashed_pass1 = get_pass_hash(pass_num.pass1)
    hashed_pass2 = get_pass_hash(pass_num.pass2)
    hashed_pass3 = get_pass_hash(pass_num.pass3)
    hashed_pass4 = get_pass_hash(pass_num.pass4)
    hashed_pass5 = get_pass_hash(pass_num.pass5)

    result = cre_pass(USER, in_apikey(API_KEY), hashed_pass0, hashed_pass1, hashed_pass2, hashed_pass3, hashed_pass4, hashed_pass5)

    if result:
        return True
    else:
        return False

@app.post("/app/chkPass/pass/", dependencies=[Depends(get_active_auth)]) # @app패스워드 검증
async def check_pass(pass_num: passNum):
    passd = [pass_num.pass0, pass_num.pass1, pass_num.pass2, pass_num.pass3, pass_num.pass4, pass_num.pass5]
    result = userPassAtuth(USER, in_apikey(API_KEY))
    i = 0
    for i in range(6):
        if verify_password(passd[i], result[0][i]) == False: # 패스워드가 맞지 않으면 멈춤
            break
        i += 1
    if i == 6: # 패스워드가 모두 맞으면
        return True
    else:
        return False

@app.get("/app/getSubClass/", dependencies=[Depends(get_active_auth)]) # 분류 값 반환
async def get_subclass():
    result = getSubclass()
    return {result}

@app.get("/app/getSource/", dependencies=[Depends(get_active_auth)]) # @app 출처 값 반환
async def get_Souce():
    result = getSource()
    return {result}

@app.get("/app/get_tags/", dependencies=[Depends(get_active_auth)]) # @app 태그 값 반환
async def get_tags():
    result = getTags()
    return {result}

@app.get("/app/get_taglists/{vals}", dependencies=[Depends(get_active_auth)]) # @app 위젯용 태그list VALUE 반환
async def get_taglists(vals: str):
    result = get_widget_tag(vals)
    return {result}

@app.get("/app/getSubclass_it/{vals}", dependencies=[Depends(get_active_auth)]) # @app 분류명 검색
async def get_subclass_it(vals: str):
    result = getSubclassit(vals)
    return {result}


#@app.exception_handler(HTTPException)ㅁ
#async def http_exception_handler(request: Request, exc: HTTPException):
#    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)