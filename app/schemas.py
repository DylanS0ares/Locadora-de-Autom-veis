from pydantic import BaseModel

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