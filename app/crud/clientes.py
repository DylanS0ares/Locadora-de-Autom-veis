from app.models import Cliente
from app.schemas import ClienteCreate, ClienteUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session


def lista_clientes(db: Session):
    clientes = db.scalars(
        select(Cliente)
    ).all()

    return clientes


def criar_cliente(
    db: Session,
    cliente: ClienteCreate
):
    email_existente = db.scalar(
        select(Cliente).where(Cliente.email == cliente.email)
    )

    if email_existente:
        return None

    novo_cliente = Cliente(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session
):
    cliente_existente = db.scalar(
        select(Cliente).where(Cliente.id == cliente_id)
    )

    if not cliente_existente:
        return False

    cliente_existente.nome = cliente.nome
    cliente_existente.email = cliente.email
    cliente_existente.telefone = cliente.telefone

    db.commit()
    db.refresh(cliente_existente)

    return cliente_existente


def deletar_cliente(
    cliente_id: int,
    db: Session
):
    cliente = db.scalar(
        select(Cliente).where(Cliente.id == cliente_id)
    )

    if not cliente:
        return False

    db.delete(cliente)
    db.commit()

    return True


def listar_locacoes_cliente(
    cliente_id: int,
    db: Session
):
    cliente = db.scalar(
        select(Cliente).where(Cliente.id == cliente_id)
    )

    if not cliente:
        return False

    return cliente.locacoes