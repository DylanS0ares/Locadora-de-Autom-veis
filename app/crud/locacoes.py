from app.models import Locacao, Cliente, Veiculo
from app.schemas import LocacaoCreate, LocacaoUpdate

from sqlalchemy import select
from sqlalchemy.orm import Session


def lista_locacoes(db: Session):
    locacoes = db.scalars(
        select(Locacao)
    ).all()

    return locacoes


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
    db.commit()
    db.refresh(nova_locacao)

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

    db.commit()
    db.refresh(locacao_existente)

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
    db.commit()

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

    db.commit()
    db.refresh(veiculo)

    return veiculo