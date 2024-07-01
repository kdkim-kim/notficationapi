from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.security import APIKeyHeader
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from passlib.context import CryptContext

from app.config.excuteSL import userAPIkey, userPasschk, cre_pass
from app.config.schema import passNum

#class passNum(BaseModel):
#    pass0:Optional[int|str] = None
#    pass1:Optional[int|str] = None
#    pass2:Optional[int|str] = None
#    pass3:Optional[int|str] = None
#    pass4:Optional[int|str] = None
#    pass5:Optional[int|str] = None


app = FastAPI()

API_KEY = None # 보안 키
API_KEY_NAME = "access-token" # 키 이름
USER = None # 사용자명
USER_KEY_NAME ="users" # 사용자명 이름
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False) # KEY HEADER
username = APIKeyHeader(name=USER_KEY_NAME, auto_error=False) # USER HEADER

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #

def in_apikey(api_key_: str):
    return api_key_.split(" ")[0]

def get_pass_hash(password): # 패스워드 해시 값 반환
    return bcrypt_context.hash(password)

async def get_api_key(api_key_: str = Depends(api_key_header), username: str = Depends(username)):
    #api_key_var_ = in_apikey(api_key_) # DB 자료 비교용 키값
    #print(api_key_var_)
    result = userAPIkey(username, in_apikey(api_key_)) # 관리자로 부터 할당 받은 사용자명과 보안키 값 검증
    if result:
        global API_KEY, USER
        API_KEY = api_key_ # 보안키 값을 전역변수에 할당
        USER = username
        return
    else:
        raise HTTPException(status_code=400, detail="Not valid")

async def get_active_auth(api_key: str = Depends(api_key_header)): # 접속시 할당 받은 키 값과 접속프로그램의 키캆 비교
    global API_KEY, USER
    print(api_key, API_KEY)
    if API_KEY == api_key:
        return
    else:
        API_KEY = None
        USER = None
        raise HTTPException(status_code=400, detail="Not valid")

@app.get("/connect/") # 최초접속 USER와 KEY 값 검증
async def connect(api_key: str = Depends(get_api_key), username: str= Depends(username)):
    return {"Connected : "}

@app.get("/app/chkExpass/") # 패스워드 유무 체크
async def chk_pass_count(api_key: str = Depends(get_active_auth)):
    result = userPasschk(USER, in_apikey(API_KEY))
    return {result}

@app.post("/app/crePass/", dependencies=[Depends(get_active_auth)])
async def create_pass(pass_num: passNum):
    hashed_pass0 = get_pass_hash(pass_num.pass0)
    hashed_pass1 = get_pass_hash(pass_num.pass1)
    hashed_pass2 = get_pass_hash(pass_num.pass2)
    hashed_pass3 = get_pass_hash(pass_num.pass3)
    hashed_pass4 = get_pass_hash(pass_num.pass4)
    hashed_pass5 = get_pass_hash(pass_num.pass5)

    result = cre_pass(USER, API_KEY, hashed_pass0, hashed_pass1, hashed_pass2, hashed_pass3, hashed_pass4, hashed_pass5)

    if result:
        print("OK")
        return True
    else:
        return False


    #@app.exception_handler(HTTPException)
#async def http_exception_handler(request: Request, exc: HTTPException):
#    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)