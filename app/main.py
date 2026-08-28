from fastapi import FastAPI
from .routers import veiculos,clientes,locacoes

app = FastAPI()

app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(locacoes.router)
