import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Usuario
from app.password import hash_senha
from app.security import criar_token


@pytest.fixture
def client(tmp_path):

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

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Usuário admin para os testes
    db = TestingSessionLocal()

    usuario_admin = Usuario(
        nome="Admin Teste",
        email="admin@teste.com",
        senha_hash=hash_senha("12345678"),
        tipo="admin"
    )

    db.add(usuario_admin)
    db.commit()
    db.refresh(usuario_admin)
    db.close()

    # Gera JWT para o usuário de teste
    token_admin = criar_token({
        "sub": str(usuario_admin.id),
        "tipo": usuario_admin.tipo
    })

    with TestClient(app) as test_client:

        test_client.headers.update({
            "Authorization": f"Bearer {token_admin}"
        })

        yield test_client

    app.dependency_overrides.clear()
    engine.dispose()