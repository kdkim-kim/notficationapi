from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.security import APIKeyHeader
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from passlib.context import CryptContext

from app.config.excuteSL import userAPIkey, userPasschk, cre_pass

class passNum(BaseModel):
    pass0:Optional[int|str] = None
    pass1:Optional[int|str] = None
    pass2:Optional[int|str] = None
    pass3:Optional[int|str] = None
    pass4:Optional[int|str] = None
    pass5:Optional[int|str] = None


app = FastAPI()

API_KEY = None
API_KEY_NAME = "access-token"
USER = None
USER_KEY_NAME ="users"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
username = APIKeyHeader(name=USER_KEY_NAME, auto_error=False)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_pass_hash(password):
    return bcrypt_context.hash(password)

async def get_api_key(api_key_: str = Depends(api_key_header), username: str = Depends(username)):
    result = userAPIkey(username, api_key_)
    if result:
        global API_KEY, USER
        API_KEY = api_key_
        print(API_KEY)
        USER = username
        return
    else:
        raise HTTPException(status_code=400, detail="Not valid")

async def get_active_auth(api_key: str = Depends(api_key_header)):
    print(API_KEY, api_key)
    if API_KEY == api_key:
        print("auth success")
        return
    else:
        raise HTTPException(status_code=400, detail="Not valid")

@app.get("/connect/")
async def connect(api_key: str = Depends(get_api_key), username: str= Depends(username)):
    return {"Connected : "}

@app.get("/app/chkExpass/")
async def chk_pass_count(api_key: str = Depends(get_active_auth)):
    result = userPasschk(USER, API_KEY)
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