from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.crud import veiculos as crud_veiculos
from ..database import get_db
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
    return crud_veiculos.listar_veiculos(db)




@router.get("/disponiveis",response_model=list[VeiculoSchema])
def listar_veiculos_disponiveis(
    db: Session = Depends(get_db)
):
    return crud_veiculos.listar_veiculos_disponiveis(db)
    


@router.get("/{veiculo_id}",response_model = VeiculoSchema)
def buscar_veiculo(veiculo_id:int,
                   db:Session = Depends(get_db)):
    veiculo = crud_veiculos.buscar_veiculo(db,veiculo_id)
    if not veiculo:
        raise HTTPException(
            status_code=404,
            detail="Veículo não encontrado"
        )
        
    return veiculo


@router.post("/",response_model=VeiculoSchema)

def criar_veiculos(
    veiculo: VeiculoCreate,
    db : Session = Depends(get_db)
):
    novo_veiculo = crud_veiculos.criar_veiculo(db,veiculo)

    if not novo_veiculo:
        raise HTTPException(
            status_code=404,
            detail="Já existe um veículo com essa placa"
        )
       
    return novo_veiculo

@router.put("/{veiculo_id}", response_model=VeiculoSchema)

def atualizar_veiculo(
    veiculo_id: int,
    veiculo: VeiculoUpdate,
    db: Session = Depends(get_db)
):
    veiculo_existente = crud_veiculos.atualizar_veiculo(db,veiculo_id,veiculo)

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
    crud_veiculos.deletar_veiculo(db,veiculo_id)
    return{"mensagem": "Veículo deletado com sucesso"}     



