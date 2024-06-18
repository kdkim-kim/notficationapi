import json
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
secret_file = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(secret_file).read())
db = secrets["DB"]

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db.get('User')}:{db.get('Password')}@{db.get('Host')}:{db.get('Port')}/{db.get('Database')}?charset=utf8"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
