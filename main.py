from typing import Union
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.security import APIKeyHeader
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from passlib.context import CryptContext

from app.config.excuteSL import schema_auth,schema_data, schema_in, schema_del
from app.config.schema import passNum,  crePass, think_, search_

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
    result = schema_auth.userAPIkey(username, in_apikey(api_key_)) # 관리자로 부터 할당 받은 사용자명과 보안키 값 검증
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
    result = schema_auth.userPasschk(USER, in_apikey(API_KEY))
    schema_auth.create_tables()
    return {result}

@app.post("/app/crePass/", dependencies=[Depends(get_active_auth)]) # @app 패스워드 생성
async def create_pass(pass_num: passNum):
    hashed_pass0 = get_pass_hash(pass_num.pass0)
    hashed_pass1 = get_pass_hash(pass_num.pass1)
    hashed_pass2 = get_pass_hash(pass_num.pass2)
    hashed_pass3 = get_pass_hash(pass_num.pass3)
    hashed_pass4 = get_pass_hash(pass_num.pass4)
    hashed_pass5 = get_pass_hash(pass_num.pass5)

    result = schema_auth.cre_pass(USER, in_apikey(API_KEY), hashed_pass0, hashed_pass1, hashed_pass2, hashed_pass3, hashed_pass4, hashed_pass5)

    if result:
        return True
    else:
        return False

@app.post("/app/crePass/EDIT/", dependencies=[Depends(get_active_auth)]) # @app 패스워드 변경
async def edit_passNum(pass_num: crePass):
    hashed_pass0 = get_pass_hash(pass_num.pass0)
    hashed_pass1 = get_pass_hash(pass_num.pass1)
    hashed_pass2 = get_pass_hash(pass_num.pass2)
    hashed_pass3 = get_pass_hash(pass_num.pass3)
    hashed_pass4 = get_pass_hash(pass_num.pass4)
    hashed_pass5 = get_pass_hash(pass_num.pass5)

    result = schema_auth.edit_passNum(USER, in_apikey(API_KEY), hashed_pass0, hashed_pass1, hashed_pass2, hashed_pass3, hashed_pass4, hashed_pass5)
    if result:
        return True
    else:
        return False

@app.post("/app/chkPass/pass/", dependencies=[Depends(get_active_auth)]) # @app패스워드 검증
async def check_pass(pass_num: passNum):
    passd = [pass_num.pass0, pass_num.pass1, pass_num.pass2, pass_num.pass3, pass_num.pass4, pass_num.pass5]
    print(passd)
    result = schema_auth.userPassAtuth(USER, in_apikey(API_KEY))
    i = 0
    for i in range(6):
        if verify_password(passd[i], result[0][i]) == False: # 패스워드가 맞지 않으면 멈춤
            break
        i += 1
    if i == 6: # 패스워드가 모두 맞으면
        print("PASS")
        return True
    else:
        print("WRONG")
        return False

############ 검색 ################
@app.get("/app/get_taglists/{vals}", dependencies=[Depends(get_active_auth)]) # @app 위젯용 태그list VALUE 반환
async def get_taglists(vals: str):
    result = schema_data.get_widget_tag(vals)
    return {result}

@app.get("/app/getDataId/all/{kind}", dependencies=[Depends(get_active_auth)]) # @app ID 로 데이타 값 조회
async def getDataId_all(kind: str, qid: int):
    result = schema_data.get_data_all(kind, qid)
    return {result}

@app.get("/app/getData/{kind}", dependencies=[Depends(get_active_auth)]) # @app 단일 테이블 의 모든 값 또는 특정 값
async def getData(kind: str, q:Union[str, None] = None): # ?q= 인자는 None 가능
    result = schema_data.get_data(kind, q)
    return {result}

@app.post("/app/searchResultList/", dependencies=[Depends(get_active_auth)]) # @app 검색
async def searchResultList(search: search_):
    search_tag_0 = search.search_tag_0
    search_tag_1 = search.search_tag_1
    search_tag_2 = search.search_tag_2
    search_tag_3 = search.search_tag_3
    search_tag_4 = search.search_tag_4
    search_subclass = search.search_subclass
    search_source = search.search_source

    result = schema_data.get_search_list(search_tag_0, search_tag_1, search_tag_2, search_tag_3, search_tag_4, search_subclass, search_source)
    return {result}

################# 입력 #####################
@app.get("/app/inSubData/{kind}", dependencies=[Depends(get_active_auth)]) # @app 분류 / 출처 등록
async def inSubData(kind: str, val: str):
    result = schema_in.in_sub_data(kind, val)
    return {result}

@app.get("/app/inThinkTag/", dependencies=[Depends(get_active_auth)]) # @app 분류list
async def inThinkTag(th_id: int, tag: int):
    print(th_id, tag)
    result = schema_in.in_think_tag(th_id, tag)
    return {result}

@app.post("/app/inThinkups/", dependencies=[Depends(get_active_auth)]) # @app 내용 입력
async def inThinkups(in_think: think_):
    title = in_think.title
    contents = in_think.contents
    think_class = in_think.think_class
    think_source = in_think.think_source
    think_filePath = in_think.think_filePath
    think_fileName = in_think.think_fileName
    print(contents)
    result = schema_in.in_thinks(title, contents, think_class, think_source, think_filePath, think_fileName)
    return {result}

################## 수정 ###################
@app.post("/app/updateThinks/", dependencies=[Depends(get_active_auth)]) # @app 패스워드 입력
async def updateThinks(in_think: think_):
    think_id = in_think.think_id
    title = in_think.title
    contents = in_think.contents
    think_class = in_think.think_class
    think_source = in_think.think_source
    think_filePath = in_think.think_filePath
    think_fileName = in_think.think_fileName
    print(contents)
    result = schema_in.update_thinks(think_id, title, contents, think_class, think_source, think_filePath, think_fileName)
    return {result[0]}

################### 삭제 ###################
@app.get("/app/data_Controls/delete/{kind}", dependencies=[Depends(get_active_auth)]) # @app 분류 / 출처 삭제
async def data_Controls_delete(kind: str, val):
    result = schema_del.del_data_(kind, val)
    return {result}
#@app.exception_handler(HTTPException)ㅁ
#async def http_exception_handler(request: Request, exc: HTTPException):
#    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)