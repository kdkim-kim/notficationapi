from sqlmodel import SQLModel, Field
from datetime import datetime

class UserBase(SQLModel):
    username: str
    email: str
    last_login: datetime
    is_admin: bool

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)