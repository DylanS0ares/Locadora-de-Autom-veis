from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:123@127.0.0.1:5433/locadora"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "options": "-c lc_messages=C"
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()