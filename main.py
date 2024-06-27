from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.security import APIKeyHeader
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config.excuteSL import userAPIkey

app = FastAPI()

API_KEY = None
API_KEY_NAME = "access-token"
USER = None
USER_KEY_NAME ="users"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
username = APIKeyHeader(name=USER_KEY_NAME, auto_error=False)

async def get_api_key(api_key_: str = Depends(api_key_header), username: str = Depends(username)):
    result = userAPIkey(username, api_key_)
    if result:
        API_KEY = api_key_
        USER = username
        print(API_KEY, USER)
        return
    else:
        raise HTTPException(status_code=400, detail="Not valid API key")

@app.get("/connect/")
async def connect(api_key: str = Depends(get_api_key), username: str= Depends(username)):
    return {"Connected : "}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)