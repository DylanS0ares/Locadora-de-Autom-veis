from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import clientes as crud_clientes
from ..database import get_db
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
def lista_clientes(
    db: Session = Depends(get_db)
):
    return crud_clientes.lista_clientes(db)


@router.post("/", response_model=ClienteSchema)
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    novo_cliente = crud_clientes.criar_cliente(db, cliente)

    if not novo_cliente:
        raise HTTPException(
            status_code=400,
            detail="Cliente já cadastrado"
        )

    return novo_cliente


@router.put("/{cliente_id}", response_model=ClienteSchema)
def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db)
):
    cliente_existente = crud_clientes.atualizar_cliente(
        cliente_id,
        cliente,
        db
    )

    if not cliente_existente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return cliente_existente


@router.delete("/{cliente_id}")
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente = crud_clientes.deletar_cliente(
        cliente_id,
        db
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return {"mensagem": "Cliente deletado com sucesso"}


@router.get("/{cliente_id}/locacoes")
def listar_locacoes_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    locacoes = crud_clientes.listar_locacoes_cliente(
        cliente_id,
        db
    )

    if locacoes is False:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return locacoes