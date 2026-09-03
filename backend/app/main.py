from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import veiculos, clientes, locacoes, usuarios

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tudo liberado
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(locacoes.router)
app.include_router(usuarios.router)