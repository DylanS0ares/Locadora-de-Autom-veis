from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate
from app.password import hash_senha


def criar_usuario(db:Session, usuario: UsuarioCreate):
    novo_usuario = Usuario(
        nome= usuario.nome,
        email = usuario.email,
        senha_hash = hash_senha(usuario.senha),
        tipo="cliente"
    )
    db.add(novo_usuario)

    try:
        db.commit()
        db.refresh(novo_usuario)
    except IntegrityError:
        db.rollback()
        return None
    return novo_usuario

def buscar_usuario_por_email(db:Session,email:str):
    return db.scalar(
        select(Usuario).where(Usuario.email==email)
    )

def criar_admin(db:Session, usuario:UsuarioCreate):
    novo_usuario =Usuario(
        nome = usuario.nome,
        email = usuario.email,
        senha_hash = hash_senha(usuario.senha),
        tipo="admin"

    )
    db.add(novo_usuario)
    try:
        db.commit()
        db.refresh(novo_usuario)
    except IntegrityError:
        db.rollback()
        return None
    
    return novo_usuario

def buscar_usuario_por_id(db:Session , usuario_id:int):
    return db.scalar(
        select(Usuario).where(Usuario.id == usuario_id)
    )