from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI ,
    connect_args={"check_same_thread": False}, # only for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
