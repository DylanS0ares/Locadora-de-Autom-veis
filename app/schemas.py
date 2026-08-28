from pydantic import BaseModel,Field,model_validator
from datetime import datetime

class VeiculoSchema(BaseModel):
    modelo : str
    marca : str
    ano : int
    placa : str
    disponivel : bool

class VeiculoCreate(BaseModel):
    modelo : str = Field(min_length=2)
    marca : str = Field(min_length=2)
    ano : int = Field(ge=1900, le=2026)
    placa : str = Field(min_length=7,max_length=7)
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
    valor: float = Field(gt=0)

    @model_validator(mode="after")

    def validar_datas(self):
        if self.data<=self.data_inicio:
            raise ValueError(
                "A data de fim deve ser posterior à data de início"
            )
        return self

class LocacaoUpdate(BaseModel):
    cliente_id: int
    veiculo_id: int
    data_inicio: datetime
    data_fim: datetime
    valor: float