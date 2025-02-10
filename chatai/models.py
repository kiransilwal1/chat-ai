from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, validator
import os

Base = declarative_base()


class ChatPath(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    path: str = Field(unique=True)


DATABASE_URL = f"sqlite:///{os.path.expanduser('~')}/.chatai/db.sqlite"


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
