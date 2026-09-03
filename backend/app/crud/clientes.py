from app.models import Cliente
from app.schemas import ClienteCreate, ClienteUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def lista_clientes(db: Session):
    return db.scalars(
        select(Cliente)
    ).all()


def criar_cliente(
    db: Session,
    cliente: ClienteCreate
):
    novo_cliente = Cliente(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone
    )

    db.add(novo_cliente)

    try:
        db.commit()
        db.refresh(novo_cliente)

    except IntegrityError:
        db.rollback()
        return None

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

    try:
        db.commit()
        db.refresh(cliente_existente)

    except IntegrityError:
        db.rollback()
        return None

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

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        return None

    return True


def listar_locacoes_cliente(
    cliente_id: int,
    db: Session
):
    cliente = db.scalar(
        select(Cliente).where(Cliente.id == cliente_id)
    )

    if not cliente:
        return None

    return cliente.locacoes