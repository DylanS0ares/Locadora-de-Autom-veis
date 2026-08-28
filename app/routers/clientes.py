from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Cliente
from ..schemas import (
    ClienteSchema,
    ClienteCreate,
    ClienteUpdate
)

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)



@router.get("/", response_model=list[ClienteSchema])
def lista_clientes(db: Session = Depends(get_db)):
    clientes = db.scalars(
        select(Cliente)
    ).all()

    return clientes


@router.post("/", response_model=ClienteSchema)
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):

    email_existente = db.scalar(
    select(Cliente).where(Cliente.email == cliente.email)
)

    if email_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe um cliente com esse e-mail"
        )
    novo_cliente = Cliente(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


@router.put("/{cliente_id}", response_model=ClienteSchema)
def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db)
):
    cliente_existente = db.scalar(
        select(Cliente).where(Cliente.id == cliente_id)
    )

    if not cliente_existente:
        raise HTTPException(
            status_code=404,
            detail = "Cliente não encontrado"
        )
    

    cliente_existente.nome = cliente.nome
    cliente_existente.email = cliente.email
    cliente_existente.telefone = cliente.telefone

    db.commit()
    db.refresh(cliente_existente)

    return cliente_existente


@router.delete("/{cliente_id}")
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente = db.scalar(
        select(Cliente).where(Cliente.id == cliente_id)
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )
        

    db.delete(cliente)
    db.commit()

    return {"mensagem": "Cliente deletado com sucesso"}



@router.get("/{cliente_id}/locacoes")
def listar_locacoes_cliente(
    cliente_id:int,
    db: Session = Depends(get_db)
):
    cliente = db.scalar(
        select(Cliente).where(Cliente.id == cliente_id)
    )
    if not cliente:
        raise HTTPException(
            status_code = 404,
            detail= "Cliente não encontrado"
        )
    return cliente.locacoes