from typing import Union, Optional
from datetime import datetime
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from database.connect import conn

app = FastAPI()

@app.on_event("startup")
def on_startup():
    conn()

person =[]
class Person(BaseModel):
    name:str
    age:Union[int,float]
    job:Optional[str] = None
    hobby:str|None = None
    major:Union[str,None] = None

class tabName(str,Enum):
    mon = "mon"
    tue = "tue"
    wed = "wed"
    thu = "thu"
    fri = "fri"
    sat = "sat"
    sun = "sun"

@app.get("/")
async def hello():
    return {"message": "Hello World"}

@app.post("/signup")
async def signup(user:Person, item_id:int, q:str):
    person.append(user)
    return {
        "item_id": item_id,
        "person": person,
        "query": q
    }

@app.get("/items/{item_id}")
async def read_irwm(item_id: int):
    return {"item_id": item_id}
@app.get("/webtoon")
async def read_item(tab:tabName, item_id:int=1):
    return {"tab":tab,"item_id":item_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)