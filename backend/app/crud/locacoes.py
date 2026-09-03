from app.models import Locacao, Cliente, Veiculo
from app.schemas import LocacaoCreate, LocacaoUpdate

from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def lista_locacoes(db: Session):
    return db.scalars(
        select(Locacao)
    ).all()


def criar_locacao(
    db: Session,
    locacao: LocacaoCreate
):
    cliente = db.scalar(
        select(Cliente).where(
            Cliente.id == locacao.cliente_id
        )
    )

    if not cliente:
        return "cliente_nao_encontrado"

    veiculo = db.scalar(
        select(Veiculo).where(
            Veiculo.id == locacao.veiculo_id
        )
    )

    if not veiculo:
        return "veiculo_nao_encontrado"

    if not veiculo.disponivel:
        return "veiculo_indisponivel"

    nova_locacao = Locacao(
        cliente_id=locacao.cliente_id,
        veiculo_id=locacao.veiculo_id,
        data_inicio=locacao.data_inicio,
        data_fim=locacao.data_fim,
        valor=locacao.valor
    )

    veiculo.disponivel = False

    db.add(nova_locacao)

    try:
        db.commit()
        db.refresh(nova_locacao)

    except IntegrityError:
        db.rollback()
        return "erro_banco"

    return nova_locacao


def atualizar_locacao(
    locacao_id: int,
    locacao: LocacaoUpdate,
    db: Session
):
    locacao_existente = db.scalar(
        select(Locacao).where(
            Locacao.id == locacao_id
        )
    )

    if not locacao_existente:
        return "locacao_nao_encontrada"

    cliente = db.scalar(
        select(Cliente).where(
            Cliente.id == locacao.cliente_id
        )
    )

    if not cliente:
        return "cliente_nao_encontrado"

    veiculo = db.scalar(
        select(Veiculo).where(
            Veiculo.id == locacao.veiculo_id
        )
    )

    if not veiculo:
        return "veiculo_nao_encontrado"

    if (
        not veiculo.disponivel
        and veiculo.id != locacao_existente.veiculo_id
    ):
        return "veiculo_indisponivel"

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

    try:
        db.commit()
        db.refresh(locacao_existente)

    except IntegrityError:
        db.rollback()
        return "erro_banco"

    return locacao_existente


def deletar_locacao(
    locacao_id: int,
    db: Session
):
    locacao = db.scalar(
        select(Locacao).where(
            Locacao.id == locacao_id
        )
    )

    if not locacao:
        return "locacao_nao_encontrada"

    veiculo = db.scalar(
        select(Veiculo).where(
            Veiculo.id == locacao.veiculo_id
        )
    )

    if veiculo:
        veiculo.disponivel = True

    db.delete(locacao)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        return "erro_banco"

    return True


def devolver_veiculo(
    locacao_id: int,
    db: Session
):
    locacao = db.scalar(
        select(Locacao).where(
            Locacao.id == locacao_id
        )
    )

    if not locacao:
        return "locacao_nao_encontrada"

    veiculo = db.scalar(
        select(Veiculo).where(
            Veiculo.id == locacao.veiculo_id
        )
    )

    if not veiculo:
        return "veiculo_nao_encontrado"

    if veiculo.disponivel:
        return "veiculo_ja_disponivel"

    veiculo.disponivel = True

    try:
        db.commit()
        db.refresh(veiculo)

    except IntegrityError:
        db.rollback()
        return "erro_banco"

    return veiculo