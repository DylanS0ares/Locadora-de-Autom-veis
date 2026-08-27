from fastapi import FastAPI,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Veiculo
from .schemas import VeiculoSchema,VeiculoCreate,VeiculoUpdate


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/veiculos",response_model=list[VeiculoSchema])

def lista_veiculos(db:Session = Depends(get_db)):
    veiculos = db.scalars(
        select(Veiculo)).all()
    return veiculos

@app.post("/veiculos",response_model=VeiculoSchema)

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
        db.add(novo_veiculo)
        db.commit()
        db.refresh(novo_veiculo)

        return novo_veiculo


@app.put("/veiculos/{veiculo_id}", response_model=VeiculoSchema)

def atualizar_veiculo(
    veiculo_id: int,
    veiculo: VeiculoUpdate,
    db: Session = Depends(get_db)
):
    veiculo_existente = db.scalar(
        select(Veiculo).where(Veiculo.id == veiculo_id)
    )

    if not veiculo_existente:
        return {"erro": "Veículo não encontrado"}

    veiculo_existente.modelo = veiculo.modelo
    veiculo_existente.marca = veiculo.marca
    veiculo_existente.ano = veiculo.ano
    veiculo_existente.placa = veiculo.placa
    veiculo_existente.disponivel = veiculo.disponivel

    db.commit()
    db.refresh(veiculo_existente)

    return veiculo_existente

@app.delete("/veiculos/{veiculo_id}")

def deletar_veiculo(
    veiculo_id :int,
    db:Session =Depends(get_db)
):
    veiculo = db.scalar(select(Veiculo).where(Veiculo.id == veiculo_id))

    if not veiculo:
     return {"erro": "Veiculo não encontrado"}

    db.delete(veiculo)
    db.commit()

    return{"mensagem": "Veículo deletado com sucesso"}     
     





def inicio():
    return ("Mensagem:" "API da Locadora funcionando!")