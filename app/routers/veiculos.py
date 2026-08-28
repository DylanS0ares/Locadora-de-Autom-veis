from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Veiculo
from ..schemas import (
    VeiculoSchema,
    VeiculoCreate,
    VeiculoUpdate,
)

router = APIRouter(
    prefix = "/veiculos",
    tags=["Veículos"]
)


@router.get("/",response_model=list[VeiculoSchema])

def lista_veiculos(db:Session = Depends(get_db)):
    veiculos = db.scalars(
        select(Veiculo)).all()
    return veiculos

@router.post("/",response_model=VeiculoSchema)

def criar_veiculos(
    veiculo: VeiculoCreate,
    db : Session = Depends(get_db)
):
        novo_veiculo = Veiculo(
             modelo = veiculo.modelo,
             marca = veiculo.marca,
             ano = veiculo.ano,
             placa = veiculo.placa,
             disponivel = veiculo.disponivel
        )
        placa_existente = db.scalar(
        select(Veiculo).where(Veiculo.placa == veiculo.placa)
        )

        if placa_existente:
            raise HTTPException(
                status_code=400,
                detail="Já existe um veículo com essa placa"
            )
        db.add(novo_veiculo)
        db.commit()
        db.refresh(novo_veiculo)

        return novo_veiculo


@router.put("/{veiculo_id}", response_model=VeiculoSchema)

def atualizar_veiculo(
    veiculo_id: int,
    veiculo: VeiculoUpdate,
    db: Session = Depends(get_db)
):
    veiculo_existente = db.scalar(
        select(Veiculo).where(Veiculo.id == veiculo_id)
    )

    if not veiculo_existente:
        raise HTTPException(
             status_code =404,
             detail = "Veículo não encontrado")
        

    veiculo_existente.modelo = veiculo.modelo
    veiculo_existente.marca = veiculo.marca
    veiculo_existente.ano = veiculo.ano
    veiculo_existente.placa = veiculo.placa
    veiculo_existente.disponivel = veiculo.disponivel

    db.commit()
    db.refresh(veiculo_existente)

    return veiculo_existente

@router.delete("/{veiculo_id}")

def deletar_veiculo(
    veiculo_id :int,
    db:Session =Depends(get_db)
):
    veiculo = db.scalar(select(Veiculo).where(Veiculo.id == veiculo_id))

    if not veiculo:
     raise HTTPException(
         status_code = 404,
         detail = "Veículo não encontrado"
     )

    db.delete(veiculo)
    db.commit()

    return{"mensagem": "Veículo deletado com sucesso"}     


@router.get("/disponiveis",response_model=list[VeiculoSchema])
def listar_veiculos_disponiveis(
    db: Session = Depends(get_db)
):
    veiculos = db.scalars(
        select(Veiculo).where(Veiculo.disponivel==True)    
        ).all()

    return veiculos

