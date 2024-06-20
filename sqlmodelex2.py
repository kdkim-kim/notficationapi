import json, os
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select
from pymysql import connect

class tags(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    
class Users(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

hero_1 = Users(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Users(name="Spider-Boy", secret_name="Pedro Parqueador", age=28)
hero_3 = Users(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
secret_file = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(secret_file).read())
db = secrets["DB"]

DATABASE_URL = f"mysql+pymysql://{db.get('User')}:{db.get('Password')}@{db.get('Host')}:{db.get('Port')}/{db.get('Database')}?charset=utf8"

engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)

#with Session(engine) as session:
#    session.add(hero_1)
#    session.add(hero_2)
#    session.add(hero_3)
#    session.commit()

with Session(engine) as session:
    statement = select(Users)
    hero = session.exec(statement).all()
    print(hero)