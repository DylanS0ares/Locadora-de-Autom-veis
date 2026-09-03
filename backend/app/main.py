from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import veiculos, clientes, locacoes, usuarios

app = FastAPI()

# Apenas o CORSMiddleware - ele já trata OPTIONS automaticamente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(locacoes.router)
app.include_router(usuarios.router)