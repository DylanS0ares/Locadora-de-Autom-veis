from .database import engine, Base, SessionLocal
from .models import Veiculo, Cliente, Locacao
from sqlalchemy import select


# Cria as tabelas no banco
Base.metadata.create_all(engine)


# Cria uma sessão
db = SessionLocal()

cliente = db.scalar(
    select(Cliente).where(Cliente.id == 1)
)

print(cliente.nome)
print(cliente.locacoes[0].id)
print(cliente.locacoes[0].cliente_id)
print(cliente.locacoes[0].veiculo_id)
print(cliente.locacoes[0].valor)



db.close()
