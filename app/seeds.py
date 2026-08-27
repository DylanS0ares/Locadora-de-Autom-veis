from .database import SessionLocal
from .models import Veiculo,Cliente,Locacao
from datetime import datetime

db = SessionLocal()

clientes = [
    Cliente(
        nome="João Silva",
        email="joao@email.com",
        telefone="32999999999"
    ),
    Cliente(
        nome="Maria Souza",
        email="maria@email.com",
        telefone="32988888888"
    ),
    Cliente(
        nome="Carlos Oliveira",
        email="carlos@email.com",
        telefone="32977777777"
    )
]
veiculos = [
    Veiculo(
        modelo="Civic",
        marca="Honda",
        ano=2024,
        placa="ABC1234"
    ),
    Veiculo(
        modelo="Corolla",
        marca="Toyota",
        ano=2023,
        placa="DEF5678"
    ),
    Veiculo(
        modelo="Onix",
        marca="Chevrolet",
        ano=2022,
        placa="GHI9012"
    )
]

locacao = Locacao(
    cliente=clientes[0],
    veiculo=veiculos[1],
    data_inicio=datetime(2026, 8, 27, 10, 0),
    data_fim=datetime(2026, 8, 30, 10, 0),
    valor=450.00
)

db.add_all(clientes)
db.add_all(veiculos)
db.commit()

db.add(locacao)
db.commit()