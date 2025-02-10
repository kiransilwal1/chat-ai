from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_engine()
        return cls._instance

    def _init_engine(self):
        DATABASE_URL = f"sqlite:///{os.path.expanduser('~')}/.chatai/db.sqlite"
        self.engine = create_engine(DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()
