from fastapi import FastAPI,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Veiculo, Cliente,Locacao

from .schemas import (
    VeiculoSchema,
    VeiculoCreate,
    VeiculoUpdate,
    ClienteSchema,
    ClienteCreate,
    ClienteUpdate,
    LocacaoSchema,
    LocacaoCreate,
    LocacaoUpdate
)

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
     

@app.get("/clientes", response_model=list[ClienteSchema])
def lista_clientes(db: Session = Depends(get_db)):
    clientes = db.scalars(
        select(Cliente)
    ).all()

    return clientes


@app.post("/clientes", response_model=ClienteSchema)
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    novo_cliente = Cliente(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


@app.put("/clientes/{cliente_id}", response_model=ClienteSchema)
def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db)
):
    cliente_existente = db.scalar(
        select(Cliente).where(Cliente.id == cliente_id)
    )

    if not cliente_existente:
        return {"erro": "Cliente não encontrado"}

    cliente_existente.nome = cliente.nome
    cliente_existente.email = cliente.email
    cliente_existente.telefone = cliente.telefone

    db.commit()
    db.refresh(cliente_existente)

    return cliente_existente


@app.delete("/clientes/{cliente_id}")
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente = db.scalar(
        select(Cliente).where(Cliente.id == cliente_id)
    )

    if not cliente:
        return {"erro": "Cliente não encontrado"}

    db.delete(cliente)
    db.commit()

    return {"mensagem": "Cliente deletado com sucesso"}


@app.get("/locacoes",response_model=list[LocacaoSchema])
def lista_locacoes(db:Session = Depends(get_db)):
    locacoes = db.scalars(
        select(Locacao)
    ).all()

    return locacoes
@app.post("/locacoes", response_model=LocacaoSchema)
def criar_locacao(
    locacao: LocacaoCreate,
    db: Session = Depends(get_db)
):
    cliente = db.scalar(
        select(Cliente).where(Cliente.id == locacao.cliente_id)
    )

    if not cliente:
        return {"erro": "Cliente não encontrado"}

    veiculo = db.scalar(
        select(Veiculo).where(Veiculo.id == locacao.veiculo_id)
    )

    if not veiculo:
        return {"erro": "Veículo não encontrado"}

    if not veiculo.disponivel:
        return {"erro": "Veículo não está disponível"}

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


@app.put("/locacoes/{locacao_id}", response_model=LocacaoSchema)
def atualizar_locacao(
    locacao_id: int,
    locacao: LocacaoUpdate,
    db: Session = Depends(get_db)
):
    locacao_existente = db.scalar(
        select(Locacao).where(Locacao.id == locacao_id)
    )

    if not locacao_existente:
        return {"erro": "Locação não encontrada"}

    cliente = db.scalar(
        select(Cliente).where(Cliente.id == locacao.cliente_id)
    )

    if not cliente:
        return {"erro": "Cliente não encontrado"}

    veiculo = db.scalar(
        select(Veiculo).where(Veiculo.id == locacao.veiculo_id)
    )

    if not veiculo:
        return {"erro": "Veículo não encontrado"}

    if not veiculo.disponivel and veiculo.id != locacao_existente.veiculo_id:
        return {"erro": "Veículo não está disponível"}

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

@app.delete("/locacoes/{locacao_id}")
def deletar_locacao(
    locacao_id: int,
    db: Session = Depends(get_db)
):
    locacao = db.scalar(
        select(Locacao).where(Locacao.id == locacao_id)
    )

    if not locacao:
        return {"erro": "Locação não encontrada"}

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