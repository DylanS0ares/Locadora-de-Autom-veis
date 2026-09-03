from fastapi import FastAPI
from .routers import veiculos,clientes,locacoes,usuarios
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(locacoes.router)
app.include_router(usuarios.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://locadora-frontend.onrender.com",  # adicione a URL do seu frontend
        "https://locadora-backend.onrender.com",   # (opcional) se for acessar diretamente
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)