from datetime import date, time
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from backend.reunioes.model import Reuniao, BloqueioAgenda, StatusReuniaoEnum


class ReuniaoRepository:
    def __init__(self, db: Session):
        self.db = db

    # ==========================================
    # BLOQUEIOS
    # ==========================================


    def criar_bloqueio(
        self, id_usuario: int, data_dia: date, hora_inicio: time, hora_fim: time, motivo: Optional[str] = None
    ) -> BloqueioAgenda:
        bloqueio = BloqueioAgenda(
            id_usuario=id_usuario, data_dia=data_dia, hora_inicio=hora_inicio, hora_fim=hora_fim, motivo=motivo
        )
        self.db.add(bloqueio)
        self.db.commit()
        self.db.refresh(bloqueio)
        return bloqueio

    def remover_bloqueio(self, id_bloqueio: int, id_usuario: int) -> bool:
        bloqueio = self.db.query(BloqueioAgenda).filter(
            BloqueioAgenda.id_bloqueio == id_bloqueio, BloqueioAgenda.id_usuario == id_usuario
        ).first()

        if bloqueio:
            self.db.delete(bloqueio)
            self.db.commit()
            return True
        return False

    def listar_bloqueios_usuario(self, id_usuario: int, data_dia: date) -> List[BloqueioAgenda]:
        return self.db.query(BloqueioAgenda).filter(
            BloqueioAgenda.id_usuario == id_usuario, BloqueioAgenda.data_dia == data_dia
        ).all()

    def listar_bloqueios(self, id_usuario: Optional[int] = None) -> List[BloqueioAgenda]:
        query = self.db.query(BloqueioAgenda)
        if id_usuario is not None:
            query = query.filter(BloqueioAgenda.id_usuario == id_usuario)
        return query.order_by(BloqueioAgenda.data_dia.asc(), BloqueioAgenda.hora_inicio.asc()).all()

    # ==========================================
    # VERIFICAÇÕES DE DISPONIBILIDADE
    # ==========================================

    def tem_bloqueio_sobreposto(self, id_usuario: int, data_dia: date, hora_inicio: time, hora_fim: time) -> bool:
        return self.db.query(BloqueioAgenda).filter(
            BloqueioAgenda.id_usuario == id_usuario,
            BloqueioAgenda.data_dia == data_dia,
            BloqueioAgenda.hora_inicio < hora_fim,
            BloqueioAgenda.hora_fim > hora_inicio,
        ).first() is not None

    def tem_reuniao_sobreposta(
        self, id_usuario: int, data_dia: date, hora_inicio: time, hora_fim: time, ignorar_reuniao_id: Optional[int] = None
    ) -> bool:
        query = self.db.query(Reuniao).filter(
            or_(Reuniao.destinatario_id == id_usuario, Reuniao.solicitado_por_id == id_usuario),
            Reuniao.data_dia == data_dia,
            Reuniao.status.in_(
                [
                    StatusReuniaoEnum.PENDENTE,
                    StatusReuniaoEnum.CONFIRMADA,
                    StatusReuniaoEnum.REAGENDAMENTO_SOLICITADO,
                ]
            ),
            Reuniao.hora_inicio < hora_fim,
            Reuniao.hora_fim > hora_inicio,
        )
        if ignorar_reuniao_id:
            query = query.filter(Reuniao.id_reuniao != ignorar_reuniao_id)
        return query.first() is not None

    # ==========================================
    # OPERAÇÕES DE REUNIÃO
    # ==========================================

    def solicitar_reuniao(
        self,
        aluno: str,
        responsavel: str,
        turma: str,
        data_dia: date,
        hora_inicio: time,
        hora_fim: time,
        solicitado_por_id: int,
        destinatario_id: Optional[int] = True,
    ) -> Reuniao:
        reuniao = Reuniao(
            aluno=aluno,
            responsavel=responsavel,
            turma=turma,
            data_dia=data_dia,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            solicitado_por_id=solicitado_por_id,
            destinatario_id=destinatario_id,
            status=StatusReuniaoEnum.PENDENTE,
        )
        self.db.add(reuniao)
        self.db.commit()
        self.db.refresh(reuniao)
        return reuniao

    def obter_por_id(self, id_reuniao: int) -> Optional[Reuniao]:
        return self.db.query(Reuniao).filter(Reuniao.id_reuniao == id_reuniao).first()

    def atualizar_status(
        self, id_reuniao: int, novo_status: StatusReuniaoEnum, motivo: Optional[str] = None
    ) -> Optional[Reuniao]:
        reuniao = self.obter_por_id(id_reuniao)
        if reuniao:
            reuniao.status = novo_status
            if motivo:
                reuniao.motivo_reagendamento = motivo
            self.db.commit()
            self.db.refresh(reuniao)
        return reuniao

    def reagendar_reuniao(
        self,
        id_reuniao: int,
        nova_data: date,
        nova_hora_inicio: time,
        nova_hora_fim: time,
        motivo: Optional[str] = None,
    ) -> Optional[Reuniao]:
        reuniao = self.obter_por_id(id_reuniao)
        if reuniao:
            reuniao.data_dia = nova_data
            reuniao.hora_inicio = nova_hora_inicio
            reuniao.hora_fim = nova_hora_fim
            reuniao.status = StatusReuniaoEnum.PENDENTE
            if motivo:
                reuniao.motivo_reagendamento = motivo
            self.db.commit()
            self.db.refresh(reuniao)
        return reuniao

    def listar_por_usuario(self, id_usuario: int) -> List[Reuniao]:
        return self.db.query(Reuniao).filter(
            or_(Reuniao.solicitado_por_id == id_usuario, Reuniao.destinatario_id == id_usuario)
        ).order_by(Reuniao.data_dia.desc()).all()

    def listar_reunioes(self) -> List[Reuniao]:
        return self.db.query(Reuniao).options(
            joinedload(Reuniao.solicitante),
            joinedload(Reuniao.destinatario)
        ).order_by(
            Reuniao.data_dia.desc(),
            Reuniao.hora_inicio.desc()
        ).all()