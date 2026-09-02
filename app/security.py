from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.database import get_db
from app.models import Usuario
from app.crud.usuarios import buscar_usuario_por_id
from fastapi import Depends, HTTPException


SECRET_KEY = "sua-chave-secreta-aqui"
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30


http_bearer = HTTPBearer()


def criar_token(data: dict):
    dados = data.copy()

    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )

    dados.update({"exp": expiracao})

    token = jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def get_usuario_atual(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    credentials_invalidas = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise credentials_invalidas

        usuario_id = int(usuario_id)

    except (JWTError, ValueError):
        raise credentials_invalidas

    usuario = buscar_usuario_por_id(
        db,
        usuario_id
    )

    if usuario is None:
        raise credentials_invalidas

    return usuario


def get_admin_atual(
    usuario: Usuario = Depends(get_usuario_atual)
):
    if usuario.tipo != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido apenas para administradores"
        )

    return usuario