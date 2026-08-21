from datetime import date, time
from typing import List, Optional
from sqlalchemy.orm import Session

from backend.reunioes.repository import ReuniaoRepository
from backend.usuario.repository import UsuarioRepository
from backend.reunioes.model import Reuniao, BloqueioAgenda, StatusReuniaoEnum


class ReuniaoService:
    def __init__(self, db: Session):
        self.reuniao_repo = ReuniaoRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    # ==========================================
    # BLOQUEIOS
    # ==========================================

    def criar_bloqueio(
        self, id_usuario: int, data_dia: date, hora_inicio: time, hora_fim: time, motivo: Optional[str] = None
    ) -> BloqueioAgenda:
        if hora_inicio >= hora_fim:
            raise ValueError("Hora inicial deve ser menor que a final.")
        if not self.usuario_repo.obter_por_id(id_usuario):
            raise ValueError("Usuário não encontrado.")

        return self.reuniao_repo.criar_bloqueio(id_usuario, data_dia, hora_inicio, hora_fim, motivo)

    def remover_bloqueio(self, id_bloqueio: int, id_usuario: int) -> None:
        sucesso = self.reuniao_repo.remover_bloqueio(id_bloqueio, id_usuario)
        if not sucesso:
            raise ValueError("Bloqueio não encontrado ou permissão negada.")

    def listar_bloqueios(self, id_usuario: Optional[int] = None) -> List[BloqueioAgenda]:
        return self.reuniao_repo.listar_bloqueios(id_usuario=id_usuario)

    # ==========================================
    # AGENDAMENTO
    # ==========================================
  

    def agendar_reuniao(
        self,
        aluno: str,
        responsavel: str,
        turma: str,
        data_dia: date,
        hora_inicio: time,
        hora_fim: time,
        solicitado_por_id: int,
        destinatario_id: Optional[int] = None,
    ) -> Reuniao:
        if hora_inicio >= hora_fim:
            raise ValueError("Hora inicial deve ser menor que a final.")

        if not self.usuario_repo.obter_por_id(solicitado_por_id):
            raise ValueError("Solicitante não encontrado.")

        if destinatario_id:
            if not self.usuario_repo.obter_por_id(destinatario_id):
                raise ValueError("Destinatário não encontrado.")
            self._validar_disponibilidade(destinatario_id, data_dia, hora_inicio, hora_fim)

        self._validar_disponibilidade(solicitado_por_id, data_dia, hora_inicio, hora_fim)

        return self.reuniao_repo.solicitar_reuniao(
            aluno, responsavel, turma, data_dia, hora_inicio, hora_fim, solicitado_por_id, destinatario_id
        )

    # ==========================================
    # FLUXO DE STATUS
    # ==========================================

  

    def confirmar_reuniao(self, id_reuniao: int, id_usuario_acao: int) -> Reuniao:
        reuniao = self._obter_reuniao_ou_erro(id_reuniao)

        if reuniao.destinatario_id and reuniao.destinatario_id != id_usuario_acao:
            raise ValueError("Apenas o destinatário pode confirmar a reunião.")

        if reuniao.status not in (StatusReuniaoEnum.PENDENTE, StatusReuniaoEnum.REAGENDAMENTO_SOLICITADO):
            raise ValueError(f"Não é possível confirmar uma reunião com status '{reuniao.status.value}'.")

        return self.reuniao_repo.atualizar_status(id_reuniao, StatusReuniaoEnum.CONFIRMADA)

    def recusar_reuniao(self, id_reuniao: int, id_usuario_acao: int, motivo: Optional[str] = None) -> Reuniao:
        reuniao = self._obter_reuniao_ou_erro(id_reuniao)

        if id_usuario_acao not in (reuniao.destinatario_id, reuniao.solicitado_por_id):
            raise ValueError("Você não tem permissão para recusar esta reunião.")

        return self.reuniao_repo.atualizar_status(
            id_reuniao=id_reuniao,
            novo_status=StatusReuniaoEnum.RECUSADA,
            motivo=motivo
        )

    def finalizar_reuniao(self, id_reuniao: int, id_usuario_acao: int) -> Reuniao:
        reuniao = self._obter_reuniao_ou_erro(id_reuniao)

        if id_usuario_acao not in (reuniao.destinatario_id, reuniao.solicitado_por_id):
            raise ValueError("Você não tem permissão para finalizar esta reunião.")

        if reuniao.status != StatusReuniaoEnum.CONFIRMADA:
            raise ValueError("Apenas reuniões confirmadas podem ser finalizadas.")

        return self.reuniao_repo.atualizar_status(id_reuniao, StatusReuniaoEnum.FINALIZADA)

    def reagendar_reuniao(
        self,
        id_reuniao: int,
        nova_data: date,
        nova_hora_inicio: time,
        nova_hora_fim: time,
        id_usuario_acao: int,
        motivo: Optional[str] = None
    ) -> Reuniao:
        reuniao = self._obter_reuniao_ou_erro(id_reuniao)

        if nova_hora_inicio >= nova_hora_fim:
            raise ValueError("Hora inicial deve ser menor que a final.")

        if id_usuario_acao not in (reuniao.destinatario_id, reuniao.solicitado_por_id):
            raise ValueError("Você não tem permissão para reagendar esta reunião.")

        if reuniao.destinatario_id:
            self._validar_disponibilidade(
                reuniao.destinatario_id, nova_data, nova_hora_inicio, nova_hora_fim, ignorar_reuniao_id=id_reuniao
            )
        self._validar_disponibilidade(
            reuniao.solicitado_por_id, nova_data, nova_hora_inicio, nova_hora_fim, ignorar_reuniao_id=id_reuniao
        )

        return self.reuniao_repo.reagendar_reuniao(
            id_reuniao=id_reuniao,
            nova_data=nova_data,
            nova_hora_inicio=nova_hora_inicio,
            nova_hora_fim=nova_hora_fim,
            motivo=motivo
        )

    # ==========================================
    # AUXILIARES
    # ==========================================

    def _obter_reuniao_ou_erro(self, id_reuniao: int) -> Reuniao:
        reuniao = self.reuniao_repo.obter_por_id(id_reuniao)
        if not reuniao:
            raise ValueError(f"Reunião {id_reuniao} não encontrada.")
        return reuniao

    def _validar_disponibilidade(
        self, id_usuario: int, data_dia: date, hora_inicio: time, hora_fim: time, ignorar_reuniao_id: Optional[int] = None
    ) -> None:
        if self.reuniao_repo.tem_bloqueio_sobreposto(id_usuario, data_dia, hora_inicio, hora_fim):
            raise ValueError(f"Usuário {id_usuario} possui bloqueio de agenda neste horário.")
        if self.reuniao_repo.tem_reuniao_sobreposta(id_usuario, data_dia, hora_inicio, hora_fim, ignorar_reuniao_id):
            raise ValueError(f"Usuário {id_usuario} já possui reunião agendada neste horário.")


    def listar_reunioes(self) -> List[Reuniao]:
        return self.reuniao_repo.listar_reunioes()