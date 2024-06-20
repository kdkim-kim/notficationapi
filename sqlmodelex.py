from typing import Optional

from sqlmodel import Field, SQLModel, create_engine, Session, select


class Users(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

hero_1 = Users(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Users(name="Spider-Boy", secret_name="Pedro Parqueador", age=28)
hero_3 = Users(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

engine = create_engine("sqlite:///sqlmodel_test.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()

with Session(engine) as session:
    statement = select(Users)
    hero = session.exec(statement).all()
    print(hero)