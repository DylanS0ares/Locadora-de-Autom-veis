from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models import Veiculo
from app.schemas import VeiculoCreate,VeiculoUpdate


def listar_veiculos(db: Session):
    return db.scalars(select(Veiculo)).all()

def buscar_veiculo(db:Session, veiculo_id:int):
    veiculo = db.scalar(
        select(Veiculo).where(Veiculo.id == veiculo_id)
    )
    return veiculo

def criar_veiculo(db:Session, veiculo: VeiculoCreate):
    placa_existente = db.scalar(
        select(Veiculo).where(Veiculo.placa==veiculo.placa)
    )
    if placa_existente:
        return None
    novo_veiculo = Veiculo(
        modelo=veiculo.modelo,
        marca=veiculo.marca,
        ano=veiculo.ano,
        placa=veiculo.placa,
        disponivel=veiculo.disponivel
    )

    db.add(novo_veiculo)
    db.commit()
    db.refresh(novo_veiculo)

    return novo_veiculo   

def atualizar_veiculo(
    veiculo_id: int,
    veiculo: VeiculoUpdate,
    db: Session
):
    veiculo_existente = db.scalar(
        select(Veiculo).where(Veiculo.id == veiculo_id)
    )

    if not veiculo_existente:
        return None
        

    veiculo_existente.modelo = veiculo.modelo
    veiculo_existente.marca = veiculo.marca
    veiculo_existente.ano = veiculo.ano
    veiculo_existente.placa = veiculo.placa
    veiculo_existente.disponivel = veiculo.disponivel

    db.commit()
    db.refresh(veiculo_existente)

    return veiculo_existente



def deletar_veiculo(
    veiculo_id :int,
    db:Session 
):
    veiculo = db.scalar(select(Veiculo).where(Veiculo.id == veiculo_id))

    if not veiculo:
        return False

    db.delete(veiculo)
    db.commit()

    return True


def listar_veiculos_disponiveis(
    db: Session
):
    veiculos = db.scalars(
        select(Veiculo).where(Veiculo.disponivel.is_(True))    
        ).all()

    return veiculos
