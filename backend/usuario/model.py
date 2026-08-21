from enum import Enum
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base

if TYPE_CHECKING:
    from backend.reunioes.model import Reuniao, BloqueioAgenda


class CargoEnum(str, Enum):
    ADM = "ADM"
    SECRETARIA = "SECRETARIA"
    ORIENTADORA = "ORIENTADORA"
    COORDENADORA = "COORDENADORA"
    DIRETORA = "DIRETORA"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_usuario: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo: Mapped[CargoEnum] = mapped_column(
        SQLEnum(CargoEnum, native_enum=False),
        nullable=False,
        default=CargoEnum.SECRETARIA,
    )

    reunioes_solicitadas: Mapped[List["Reuniao"]] = relationship(
        "Reuniao",
        foreign_keys="Reuniao.solicitado_por_id",
        back_populates="solicitante",
    )
    reunioes_recebidas: Mapped[List["Reuniao"]] = relationship(
        "Reuniao",
        foreign_keys="Reuniao.destinatario_id",
        back_populates="destinatario",
    )
    bloqueios: Mapped[List["BloqueioAgenda"]] = relationship(
        "BloqueioAgenda", back_populates="usuario", cascade="all, delete-orphan"
    )