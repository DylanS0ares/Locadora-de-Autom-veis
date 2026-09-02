from pydantic import BaseModel, Field, model_validator, EmailStr
from datetime import datetime


class VeiculoSchema(BaseModel):
    id: int
    modelo: str
    marca: str
    ano: int
    placa: str = Field(
        min_length=7,
        max_length=7,
        pattern=r"^([A-Z]{3}[0-9]{4}|[A-Z]{3}[0-9][A-Z][0-9]{2})$"
    )
    disponivel: bool


class VeiculoCreate(BaseModel):
    modelo: str = Field(min_length=2)
    marca: str = Field(min_length=2)
    ano: int = Field(
        ge=1900,
        le=datetime.now().year
    )
    placa: str = Field(
        min_length=7,
        max_length=7,
        pattern=r"^([A-Z]{3}[0-9]{4}|[A-Z]{3}[0-9][A-Z][0-9]{2})$"
    )
    disponivel: bool = True


class VeiculoUpdate(BaseModel):
    modelo: str = Field(min_length=2)
    marca: str = Field(min_length=2)
    ano: int = Field(
        ge=1900,
        le=datetime.now().year
    )
    placa: str = Field(
        min_length=7,
        max_length=7,
        pattern=r"^([A-Z]{3}[0-9]{4}|[A-Z]{3}[0-9][A-Z][0-9]{2})$"
    )
    disponivel: bool


class ClienteSchema(BaseModel):
    id: int
    nome: str = Field(min_length=3)
    email: EmailStr
    telefone: str = Field(
        min_length=10,
        max_length=10,
        pattern=r"^[0-9]{10}$"
    )


class ClienteCreate(BaseModel):
    nome: str = Field(min_length=3)
    email: EmailStr
    telefone: str = Field(
        min_length=10,
        max_length=10,
        pattern=r"^[0-9]{10}$"
    )


class ClienteUpdate(BaseModel):
    nome: str = Field(min_length=3)
    email: EmailStr
    telefone: str = Field(
        min_length=10,
        max_length=10,
        pattern=r"^[0-9]{10}$"
    )


class LocacaoSchema(BaseModel):
    id: int
    cliente_id: int
    veiculo_id: int
    data_inicio: datetime
    data_fim: datetime
    valor: float


class LocacaoCreate(BaseModel):
    cliente_id: int
    veiculo_id: int
    data_inicio: datetime
    data_fim: datetime
    valor: float = Field(gt=0)

    @model_validator(mode="after")
    def validar_datas(self):
        agora = datetime.now()

        if self.data_inicio < agora:
            raise ValueError(
                "A data de início não pode estar no passado"
            )

        if self.data_inicio >= self.data_fim:
            raise ValueError(
                "A data de início deve ser anterior à data de fim"
            )

        return self


class LocacaoUpdate(BaseModel):
    cliente_id: int
    veiculo_id: int
    data_inicio: datetime
    data_fim: datetime
    valor: float = Field(gt=0)

    @model_validator(mode="after")
    def validar_datas(self):
        agora = datetime.now()

        if self.data_inicio < agora:
            raise ValueError(
                "A data de início não pode estar no passado"
            )

        if self.data_inicio >= self.data_fim:
            raise ValueError(
                "A data de início deve ser anterior à data de fim"
            )

        return self