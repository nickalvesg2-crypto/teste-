from datetime import datetime, date, time
from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime, Date, Time, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator

from backend.core.database import Base

if TYPE_CHECKING:
    from backend.usuario.model import Usuario


class StatusReuniaoEnum(str, Enum):
    PENDENTE = "Pendente"
    CONFIRMADA = "Confirmada"
    RECUSADA = "Recusada"
    REAGENDAMENTO_SOLICITADO = "Reagendamento Solicitado"
    FINALIZADA = "Finalizada"


class EnumString(TypeDecorator):
    """Salva o valor do enum e aceita valores salvos em nome ou valor."""
    impl = String
    cache_ok = True

    def __init__(self, enum_cls, length=50, **kw):
        super().__init__(length=length, **kw)
        self.enum_cls = enum_cls

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, self.enum_cls):
            return value.value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        for member in self.enum_cls:
            if value == member.value or value == member.name:
                return member
        return value


class Reuniao(Base):
    __tablename__ = "reunioes"

    id_reuniao: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    aluno: Mapped[str] = mapped_column(String(150), nullable=False)
    responsavel: Mapped[str] = mapped_column(String(150), nullable=False)
    turma: Mapped[str] = mapped_column(String(50), nullable=False)

    data_dia: Mapped[date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fim: Mapped[time] = mapped_column(Time, nullable=False)

    solicitado_por_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"), nullable=False
    )
    destinatario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"), nullable=True
    )

    status: Mapped[StatusReuniaoEnum] = mapped_column(
        EnumString(StatusReuniaoEnum, length=50),
        nullable=False,
        default=StatusReuniaoEnum.PENDENTE,
    )
    motivo_reagendamento: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    solicitante: Mapped["Usuario"] = relationship(
        "Usuario", foreign_keys=[solicitado_por_id], back_populates="reunioes_solicitadas"
    )
    destinatario: Mapped[Optional["Usuario"]] = relationship(
        "Usuario", foreign_keys=[destinatario_id], back_populates="reunioes_recebidas"
    )


class BloqueioAgenda(Base):
    __tablename__ = "bloqueios_agenda"

    id_bloqueio: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False
    )

    data_dia: Mapped[date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fim: Mapped[time] = mapped_column(Time, nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="bloqueios")