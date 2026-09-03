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
    allow_origins=["http://localhost:3000", "http://localhost:3001", "https://seu-frontend.vercel.app"],  # ou ["*"] para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)