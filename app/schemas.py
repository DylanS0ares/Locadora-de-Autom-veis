from pydantic import BaseModel
from datetime import datetime

class VeiculoSchema(BaseModel):
    modelo : str
    marca : str
    ano : int
    placa : str
    disponivel : bool

class VeiculoCreate(BaseModel):
    modelo : str
    marca : str
    ano : int
    placa : str
    disponivel : bool = True

class VeiculoUpdate(BaseModel):
    modelo: str
    marca: str
    ano: int
    placa: str
    disponivel: bool

class ClienteSchema(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str

class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: str


class ClienteUpdate(BaseModel):
    nome: str
    email: str
    telefone: str

class LocacaoSchema(BaseModel):
    id:int
    cliente_id:int
    veiculo_id:int
    data_inicio:datetime
    data_fim: datetime
    valor:float

class LocacaoCreate(BaseModel):
    cliente_id:int
    veiculo_id:int
    data_inicio: datetime
    data_fim: datetime
    valor: float

class LocacaoUpdate(BaseModel):
    cliente_id: int
    veiculo_id: int
    data_inicio: datetime
    data_fim: datetime
    valor: float