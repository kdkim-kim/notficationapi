from sqlmodel import create_engine, SQLModel

database_file = "sqlite3_kim.db"  # Change this to the name of your database file
sqlite_url = f"sqlite:///{database_file}"
engine = create_engine(sqlite_url, echo=True)

def conn():
    SQLModel.metadata.create_all(engine)

