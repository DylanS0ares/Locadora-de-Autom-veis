from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from .routers import veiculos, clientes, locacoes, usuarios

app = FastAPI()

# 1. CORS com CORSMiddleware (padrão)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use "*" para teste
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MIDDLEWARE MANUAL (força os headers em TODAS as respostas)
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Rotas
app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(locacoes.router)
app.include_router(usuarios.router)