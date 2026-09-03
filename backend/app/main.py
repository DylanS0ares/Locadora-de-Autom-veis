from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import veiculos, clientes, locacoes, usuarios

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "https://locadora-frontend-u7n6.onrender.com",  # URL exata do frontend
    # ou use "*" para teste
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(locacoes.router)
app.include_router(usuarios.router)