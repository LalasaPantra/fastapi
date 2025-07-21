from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from sqlalchemy import URL
from fastapi import Depends
from .config import settings

# import ipdb

# ipdb.set_trace()

url_object = URL.create(
    "postgresql",
    username=settings.db_user,
    password=settings.db_password,  # plain (unescaped) text
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/database_name"
engine = create_engine(url_object, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
