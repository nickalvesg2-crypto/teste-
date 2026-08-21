from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.usuario.service import UsuarioService
from backend.usuario.schema import UsuarioLoginSchema
from backend.usuario.schema import (
    UsuarioCreateSchema,
    UsuarioUpdateSchema,
    UsuarioResponseSchema,
    
)

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioService:
    return UsuarioService(db)

@router.post("/login", response_model=UsuarioResponseSchema)
def login_usuario(
    payload: UsuarioLoginSchema,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.login(
        nome_usuario=payload.nome_usuario,
        senha=payload.senha
    )

@router.post("/", response_model=UsuarioResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_usuario(
    payload: UsuarioCreateSchema,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.criar_usuario(payload)


@router.get("/", response_model=List[UsuarioResponseSchema])
def listar_usuarios(service: UsuarioService = Depends(get_usuario_service)):
    return service.listar_usuarios()


@router.get("/{id_usuario}", response_model=UsuarioResponseSchema)
def buscar_usuario(
    id_usuario: int,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.buscar_por_id(id_usuario)


@router.put("/{id_usuario}", response_model=UsuarioResponseSchema)
def atualizar_usuario(
    id_usuario: int,
    payload: UsuarioUpdateSchema,
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.atualizar_usuario(id_usuario, payload)


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(
    id_usuario: int,
    service: UsuarioService = Depends(get_usuario_service)
):
    service.deletar_usuario(id_usuario)