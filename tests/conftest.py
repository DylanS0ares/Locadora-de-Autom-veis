import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


@pytest.fixture
def client(tmp_path):

    # Cria um banco SQLite exclusivo para este teste
    database_url = f"sqlite:///{tmp_path}/test.db"

    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    # Cria as tabelas neste banco novo
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    engine.dispose()