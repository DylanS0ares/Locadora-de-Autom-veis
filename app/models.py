from sqlalchemy import String, Integer, Boolean,Float,DateTime,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from .database import Base
from datetime import datetime

class Veiculo(Base):
    __tablename__ = "veiculos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    locacoes: Mapped[list["Locacao"]] = relationship(
    back_populates="veiculo")
    modelo : Mapped[str] = mapped_column(String(100))
    marca : Mapped[str] = mapped_column(String(100))
    ano: Mapped[int] = mapped_column(Integer)
    placa: Mapped[str] = mapped_column(String(100),unique=100,nullable=False)
    disponivel: Mapped[bool] = mapped_column(Boolean,default=True)
    quilometragem: Mapped[int] = mapped_column(Integer,default=0)

class Cliente(Base):
    __tablename__ = "clientes"
    id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    locacoes: Mapped[list["Locacao"]] = relationship(
        back_populates="cliente"
    )
    nome : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    telefone: Mapped[str] = mapped_column(String(100))

class Locacao(Base):
    __tablename__ = "locacoes"
    id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    cliente: Mapped["Cliente"] = relationship(back_populates="locacoes")
    veiculo: Mapped["Veiculo"] = relationship(back_populates="locacoes")
    cliente_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("clientes.id")
    )
    veiculo_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("veiculos.id")
    )
    data_inicio: Mapped[datetime] = mapped_column(DateTime)
    data_fim: Mapped[datetime] = mapped_column(DateTime)
    valor: Mapped[float] = mapped_column(Float)


class Usuario(Base):
    __tablename__ = "usuario"
    id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100),unique=True, nullable = False)
    senha_hash: Mapped[str] = mapped_column(String(255),nullable=False)
    tipo: Mapped[str] = mapped_column(String(20),default="cliente",nullable=False)
