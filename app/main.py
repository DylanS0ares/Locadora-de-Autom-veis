from fastapi import FastAPI
from .routers import veiculos,clientes,locacoes,usuarios
from .database import Base, engine
app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(locacoes.router)
app.include_router(usuarios.router)
