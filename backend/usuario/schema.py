from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from backend.usuario.model import CargoEnum


# --- ENTRADAS (Requests) ---

class UsuarioCreateSchema(BaseModel):
    nome_usuario: str = Field(..., min_length=3, max_length=100)
    senha: str = Field(..., min_length=6, max_length=255)
    cargo: CargoEnum = CargoEnum.SECRETARIA


class UsuarioUpdateSchema(BaseModel):
    nome_usuario: Optional[str] = Field(default=None, min_length=3, max_length=100)
    senha: Optional[str] = Field(default=None, min_length=6, max_length=255)
    cargo: Optional[CargoEnum] = None


class UsuarioLoginSchema(BaseModel):
    nome_usuario: str
    senha: str


# --- SAÍDAS (Responses) ---

class UsuarioResponseSchema(BaseModel):
    id_usuario: int
    nome_usuario: str
    cargo: CargoEnum

    model_config = ConfigDict(from_attributes=True)