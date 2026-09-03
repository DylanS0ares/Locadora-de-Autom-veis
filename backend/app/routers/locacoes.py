from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import locacoes as crud_locacoes
from ..database import get_db
from ..schemas import (
    LocacaoSchema,
    LocacaoCreate,
    LocacaoUpdate
)


router = APIRouter(
    prefix="/locacoes",
    tags=["Locações"]
)


@router.get("/", response_model=list[LocacaoSchema])
def lista_locacoes(
    db: Session = Depends(get_db)
):
    return crud_locacoes.lista_locacoes(db)


@router.post("/", response_model=LocacaoSchema)
def criar_locacao(
    locacao: LocacaoCreate,
    db: Session = Depends(get_db)
):
    resultado = crud_locacoes.criar_locacao(
        db,
        locacao
    )

    if resultado == "cliente_nao_encontrado":
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    if resultado == "veiculo_nao_encontrado":
        raise HTTPException(
            status_code=404,
            detail="Veículo não encontrado"
        )

    if resultado == "veiculo_indisponivel":
        raise HTTPException(
            status_code=409,
            detail="Veículo não disponível"
        )

    if resultado == "erro_banco":
        raise HTTPException(
            status_code=500,
            detail="Erro ao criar locação"
        )

    return resultado


@router.put("/{locacao_id}", response_model=LocacaoSchema)
def atualizar_locacao(
    locacao_id: int,
    locacao: LocacaoUpdate,
    db: Session = Depends(get_db)
):
    resultado = crud_locacoes.atualizar_locacao(
        locacao_id,
        locacao,
        db
    )

    if resultado == "locacao_nao_encontrada":
        raise HTTPException(
            status_code=404,
            detail="Locação não encontrada"
        )

    if resultado == "cliente_nao_encontrado":
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    if resultado == "veiculo_nao_encontrado":
        raise HTTPException(
            status_code=404,
            detail="Veículo não encontrado"
        )

    if resultado == "veiculo_indisponivel":
        raise HTTPException(
            status_code=409,
            detail="Veículo não disponível"
        )

    if resultado == "erro_banco":
        raise HTTPException(
            status_code=500,
            detail="Erro ao atualizar locação"
        )

    return resultado


@router.delete("/{locacao_id}")
def deletar_locacao(
    locacao_id: int,
    db: Session = Depends(get_db)
):
    resultado = crud_locacoes.deletar_locacao(
        locacao_id,
        db
    )

    if resultado == "locacao_nao_encontrada":
        raise HTTPException(
            status_code=404,
            detail="Locação não encontrada"
        )

    if resultado == "erro_banco":
        raise HTTPException(
            status_code=500,
            detail="Erro ao deletar locação"
        )

    return {
        "mensagem": "Locação deletada com sucesso"
    }


@router.post("/{locacao_id}/devolver")
def devolver_veiculo(
    locacao_id: int,
    db: Session = Depends(get_db)
):
    resultado = crud_locacoes.devolver_veiculo(
        locacao_id,
        db
    )

    if resultado == "locacao_nao_encontrada":
        raise HTTPException(
            status_code=404,
            detail="Locação não encontrada"
        )

    if resultado == "veiculo_nao_encontrado":
        raise HTTPException(
            status_code=404,
            detail="Veículo não encontrado"
        )

    if resultado == "veiculo_ja_disponivel":
        raise HTTPException(
            status_code=409,
            detail="Esse veículo já está disponível"
        )

    if resultado == "erro_banco":
        raise HTTPException(
            status_code=500,
            detail="Erro ao devolver veículo"
        )

    return {
        "mensagem": "Veículo devolvido com sucesso",
        "veiculo": resultado.modelo
    }