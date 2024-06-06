from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import URL
import os


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"
SQLALCHEMY_DATABASE_URL = URL.create(
    "postgresql",
    username=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    host=os.environ['DB_HOST'],
    database="postgres",
    port=int(os.environ['DB_PORT']),
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
