from models import Base, engine


def init_db():
    """Initialize the database"""
    Base.metadata.create_all(engine)
