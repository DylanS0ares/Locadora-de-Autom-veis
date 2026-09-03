from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioSchema,LoginSchema
from app.crud.usuarios import criar_usuario,buscar_usuario_por_email
from app.security import criar_token
from app.password import verificar_senha


router = APIRouter(
    prefix = "/usuarios",
    tags=["Usuários"]
)

@router.post("/",response_model=UsuarioSchema,status_code=201)

def cadastrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    novo_usuario = criar_usuario(db,usuario)

    if novo_usuario is None:
        raise HTTPException(
            status_code =400,
            detail= "Email já cadastrado"
        )
    return novo_usuario

@router.post("/login")

def login(
    dados: LoginSchema,
    db: Session = Depends(get_db)
):
    usuario = buscar_usuario_por_email(
        db,
        dados.email
    )

    if not usuario:
        raise HTTPException(
            status_code = 401,
            detail = "Email ou senha inválidos"
        )

    if not verificar_senha(
        dados.senha,
        usuario.senha_hash
    ):
        raise HTTPException(
        status_code=401,
        detail = "Email ou senha inválidos"
        )
    token = criar_token({
        "sub": str(usuario.id),
        "tipo": usuario.tipo
    })

    return{
        "access_token": token,
        "token_type": "bearer"
    }

def buscar_usuario_por_id(db: Session, usuario_id:int):
    return db.scalar(
        select(Usuario).where(Usuario.id == usuario_id)
    )
