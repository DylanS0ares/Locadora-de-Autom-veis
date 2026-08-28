from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Locacao, Cliente, Veiculo
from ..schemas import (
    LocacaoSchema,
    LocacaoCreate,
    LocacaoUpdate
)

router = APIRouter(
    prefix="/locacoes",
    tags=["Locações"]
)


@router.get("/",response_model=list[LocacaoSchema])
def lista_locacoes(db:Session = Depends(get_db)):
    locacoes = db.scalars(
        select(Locacao)
    ).all()

    return locacoes

@router.post("/", response_model=LocacaoSchema)
def criar_locacao(
    locacao: LocacaoCreate,
    db: Session = Depends(get_db)
):
    cliente = db.scalar(
        select(Cliente).where(Cliente.id == locacao.cliente_id)
    )

    if not cliente:
        raise HTTPException(
        status_code=404,
        detail="Cliente não encontrado"
    )
        
    veiculo = db.scalar(
        select(Veiculo).where(Veiculo.id == locacao.veiculo_id)
    )

    if not veiculo:
        raise HTTPException(
        status_code=404,
        detail="Veículo não encontrado"
    )

    if not veiculo.disponivel:
        raise HTTPException(
        status_code=404,
        detail="Veículo não disponivel"
    )

    nova_locacao = Locacao(
        cliente_id=locacao.cliente_id,
        veiculo_id=locacao.veiculo_id,
        data_inicio=locacao.data_inicio,
        data_fim=locacao.data_fim,
        valor=locacao.valor
    )

    veiculo.disponivel = False

    db.add(nova_locacao)
    db.commit()
    db.refresh(nova_locacao)

    return nova_locacao


@router.put("/{locacao_id}", response_model=LocacaoSchema)
def atualizar_locacao(
    locacao_id: int,
    locacao: LocacaoUpdate,
    db: Session = Depends(get_db)
):
    locacao_existente = db.scalar(
        select(Locacao).where(Locacao.id == locacao_id)
    )

    if not locacao_existente:
        raise HTTPException(
        status_code=404,
        detail="Locação não encontrada"
    )

    cliente = db.scalar(
        select(Cliente).where(Cliente.id == locacao.cliente_id)
    )

    if not cliente:
        raise HTTPException(
        status_code=404,
        detail="Cliente não encontrado"
    )

    veiculo = db.scalar(
        select(Veiculo).where(Veiculo.id == locacao.veiculo_id)
    )

    if not veiculo:
        raise HTTPException(
        status_code=404,
        detail="Veiculo não encontrado"
    )

    if not veiculo.disponivel and veiculo.id != locacao_existente.veiculo_id:
        raise HTTPException(
        status_code=404,
        detail="Veiculo não disponivel"
    )
    # Libera o veículo antigo
    veiculo_antigo = db.scalar(
        select(Veiculo).where(
            Veiculo.id == locacao_existente.veiculo_id
        )
    )

    if veiculo_antigo.id != veiculo.id:
        veiculo_antigo.disponivel = True
        veiculo.disponivel = False

    locacao_existente.cliente_id = locacao.cliente_id
    locacao_existente.veiculo_id = locacao.veiculo_id
    locacao_existente.data_inicio = locacao.data_inicio
    locacao_existente.data_fim = locacao.data_fim
    locacao_existente.valor = locacao.valor

    db.commit()
    db.refresh(locacao_existente)

    return locacao_existente

@router.delete("/{locacao_id}")
def deletar_locacao(
    locacao_id: int,
    db: Session = Depends(get_db)
):
    locacao = db.scalar(
        select(Locacao).where(Locacao.id == locacao_id)
    )

    if not locacao:
        raise HTTPException(
        status_code=404,
        detail="Locação não encontrada"
    )
    veiculo = db.scalar(
        select(Veiculo).where(
            Veiculo.id == locacao.veiculo_id
        )
    )

    if veiculo:
        veiculo.disponivel = True

    db.delete(locacao)
    db.commit()

    return {"mensagem": "Locação deletada com sucesso"}

@router.post("/{locacao_id}/devolver")
def devolver_veiculo(
    locacao_id:int,
    db:Session = Depends(get_db)
):
    locacao = db.scalar(
        select(Locacao).where(Locacao.id==locacao_id)
    )

    if not locacao:
        raise HTTPException(
            status_code = 404,
            detail = "Locação não encontrada"
        )

    veiculo = db.scalar(
        select(Veiculo).where(Veiculo.id == locacao.veiculo_id)

    )

    if not veiculo:
        raise HTTPException(
            status_code =404,
            detail = "Veículo não encontrado"
        )

    if veiculo.disponivel:
        raise HTTPException(
            status_code=400,
            detail="Esse veículo já está disponível"
        )
    veiculo.disponivel = True

    db.commit()
    db.refresh(veiculo)

    return{
        "mensagem": "Veículo devolvido com sucesso",
        "veiculo": veiculo.modelo
    }


