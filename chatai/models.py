from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
import os


class ChatPath(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    path: str = Field(unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to ChatData
    chat_data: list["ChatData"] = Relationship(back_populates="chat_path")


class ChatData(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_path_id: int = Field(foreign_key="chatpath.id")
    full_chat: str
    summary: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship back to ChatPath
    chat_path: "ChatPath" = Relationship(back_populates="chat_data")


DATABASE_URL = f"sqlite:///{os.path.expanduser('~')}/.chatai/db.sqlite"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
