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
    novo_cliente = crud_clientes.criar_cliente(
        db,
        cliente
    )

    if novo_cliente is None:
        raise HTTPException(
            status_code=409,
            detail="Já existe um cliente com esse e-mail"
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

    if cliente_existente is False:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    if cliente_existente is None:
        raise HTTPException(
            status_code=409,
            detail="Já existe um cliente com esse e-mail"
        )

    return cliente_existente


@router.delete("/{cliente_id}")
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    resultado = crud_clientes.deletar_cliente(
        cliente_id,
        db
    )

    if resultado is False:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    if resultado is None:
        raise HTTPException(
            status_code=500,
            detail="Erro ao deletar cliente"
        )

    return {
        "mensagem": "Cliente deletado com sucesso"
    }


@router.get("/{cliente_id}/locacoes")
def listar_locacoes_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    locacoes = crud_clientes.listar_locacoes_cliente(
        cliente_id,
        db
    )

    if locacoes is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return locacoes