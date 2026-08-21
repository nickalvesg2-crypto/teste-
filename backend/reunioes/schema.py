from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.usuario.schema import UsuarioResponseSchema

from backend.reunioes.model import StatusReuniaoEnum


# --- SCHEMAS DE BLOQUEIO DE AGENDA ---

class BloqueioCreateSchema(BaseModel):
    data_dia: date
    hora_inicio: time
    hora_fim: time
    motivo: Optional[str] = Field(default=None, max_length=255)


class BloqueioResponseSchema(BaseModel):
    id_bloqueio: int
    id_usuario: int
    data_dia: date
    hora_inicio: time
    hora_fim: time
    motivo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS DE REUNIÃO ---

class ReuniaoSolicitarSchema(BaseModel):
    aluno: str = Field(..., max_length=150)
    responsavel: str = Field(..., max_length=150)
    turma: str = Field(..., max_length=50)
    data_dia: date
    hora_inicio: time
    hora_fim: time
    solicitado_por_id: Optional[int] = None
    destinatario_id: Optional[int] = None


class ReuniaoReagendarSchema(BaseModel):
    nova_data: date
    nova_hora_inicio: time
    nova_hora_fim: time
    motivo: Optional[str] = Field(default=None, max_length=255)


class ReuniaoRecusarSchema(BaseModel):
    motivo: Optional[str] = Field(default=None, max_length=255)


class ReuniaoResponseSchema(BaseModel):
    id_reuniao: int

    aluno: str
    responsavel: str
    turma: str

    data_dia: date
    hora_inicio: time
    hora_fim: time

    solicitado_por_id: int
    #destinatario_id: Optional[int] = None
    destinatario_id: int | None = None

    solicitante: UsuarioResponseSchema
    destinatario: Optional[UsuarioResponseSchema] = None

    status: StatusReuniaoEnum

    motivo_reagendamento: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MotivoSchema(BaseModel):
    motivo: Optional[str] = True