from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import veiculos, clientes, locacoes, usuarios

app = FastAPI()

# 🔥 CORS PRIMEIRO (antes das rotas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://locadora-frontend-u7n6.onrender.com",  # URL DO SEU FRONTEND
        "https://locadora-backend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Depois as rotas
app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(locacoes.router)
app.include_router(usuarios.router)