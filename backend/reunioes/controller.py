from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from backend.core.database import get_db
from backend.reunioes.service import ReuniaoService
from backend.reunioes.schema import (
    BloqueioCreateSchema,
    BloqueioResponseSchema,
    MotivoSchema,  # <--- IMPORTANTE
    ReuniaoReagendarSchema,
    ReuniaoResponseSchema,
    ReuniaoSolicitarSchema,
)

router = APIRouter(prefix="/reunioes", tags=["Reuniões"])


def get_reuniao_service(db: Session = Depends(get_db)) -> ReuniaoService:
    return ReuniaoService(db)


# --- BLOQUEIOS DE AGENDA ---

@router.post("/bloqueios", response_model=BloqueioResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_bloqueio(
    payload: BloqueioCreateSchema,
    id_usuario: int,  # Em produção, extraído via token JWT
    service: ReuniaoService = Depends(get_reuniao_service)
):
    return service.criar_bloqueio(
        id_usuario=id_usuario,
        data_dia=payload.data_dia,
        hora_inicio=payload.hora_inicio,
        hora_fim=payload.hora_fim,
        motivo=payload.motivo
    )


@router.get("/bloqueios", response_model=List[BloqueioResponseSchema])
def listar_bloqueios(
    id_usuario: Optional[int] = None,
    service: ReuniaoService = Depends(get_reuniao_service)
):
    return service.listar_bloqueios(id_usuario=id_usuario)


@router.delete("/bloqueios/{id_bloqueio}", status_code=status.HTTP_204_NO_CONTENT)
def remover_bloqueio(
    id_bloqueio: int,
    id_usuario: int,
    service: ReuniaoService = Depends(get_reuniao_service)
):
    service.remover_bloqueio(id_bloqueio, id_usuario)


# --- SOLICITAÇÃO E AGENDAMENTO ---

@router.get("", response_model=List[ReuniaoResponseSchema])
def listar_reunioes(
    service: ReuniaoService = Depends(get_reuniao_service)
):
    return service.listar_reunioes()

@router.post("", response_model=ReuniaoResponseSchema, status_code=status.HTTP_201_CREATED)
def agendar_reuniao(
    payload: ReuniaoSolicitarSchema,
    solicitado_por_id: int | None = None,
    service: ReuniaoService = Depends(get_reuniao_service)
):
    remetente_id = payload.solicitado_por_id or solicitado_por_id
    if remetente_id is None:
        raise ValueError("Identificação do solicitante é obrigatória.")

    return service.agendar_reuniao(
        aluno=payload.aluno,
        responsavel=payload.responsavel,
        turma=payload.turma,
        data_dia=payload.data_dia,
        hora_inicio=payload.hora_inicio,
        hora_fim=payload.hora_fim,
        solicitado_por_id=remetente_id,
        destinatario_id=payload.destinatario_id or None,
    )


# --- FLUXO DE STATUS ---

@router.patch("/{id_reuniao}/confirmar", response_model=ReuniaoResponseSchema)
def confirmar_reuniao(
    id_reuniao: int,
    id_usuario_acao: int,
    service: ReuniaoService = Depends(get_reuniao_service)
):
    return service.confirmar_reuniao(id_reuniao, id_usuario_acao)


@router.patch("/{id_reuniao}/recusar", response_model=ReuniaoResponseSchema)
def recusar_reuniao(
    id_reuniao: int,
    id_usuario_acao: int,
    payload: Optional[MotivoSchema] = None,
    service: ReuniaoService = Depends(get_reuniao_service)
):
    motivo = payload.motivo if payload else None
    return service.recusar_reuniao(id_reuniao, id_usuario_acao, motivo)


@router.patch("/{id_reuniao}/reagendar", response_model=ReuniaoResponseSchema)
def reagendar_reuniao(
    id_reuniao: int,
    id_usuario_acao: int,
    payload: ReuniaoReagendarSchema,
    service: ReuniaoService = Depends(get_reuniao_service)
):
    return service.reagendar_reuniao(
        id_reuniao=id_reuniao,
        nova_data=payload.nova_data,
        nova_hora_inicio=payload.nova_hora_inicio,
        nova_hora_fim=payload.nova_hora_fim,
        id_usuario_acao=id_usuario_acao,
        motivo=payload.motivo
    )


@router.patch(
    "/{id_reuniao}/finalizar",
    response_model=ReuniaoResponseSchema
)
def finalizar_reuniao(
    id_reuniao: int,
    id_usuario_acao: int,
    service: ReuniaoService = Depends(get_reuniao_service)
):
    return service.finalizar_reuniao(
        id_reuniao,
        id_usuario_acao
    )