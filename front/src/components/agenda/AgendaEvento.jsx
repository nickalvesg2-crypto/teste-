import React from 'react';
import { formatarDataCurta, formatarHora } from '../../utils/data';
import './agenda.css';

function classeBadge(status) {
  const statusNormalizado = status?.toUpperCase();

  if (statusNormalizado === 'PENDENTE') return 'badge badge-pendente';
  if (statusNormalizado === 'CONFIRMADA') return 'badge badge-confirmada';
  if (statusNormalizado === 'RECUSADA') return 'badge badge-recusada';
  if (statusNormalizado === 'FINALIZADA') return 'badge badge-finalizada';
  if (statusNormalizado === 'REAGENDAMENTO_SOLICITADO' || statusNormalizado === 'REAGENDAMENTO SOLICITADO') {
    return 'badge badge-reagendamento';
  }
  return 'badge';
}

export default function AgendaEvento({
  evento,
  onConfirmar,
  onRecusar,
  onFinalizar
}) {
  const statusUpper = evento.status?.toUpperCase();

  return (
    <article className="agenda-evento">
      <div className="agenda-evento-hora">
        <strong>{formatarHora(evento.hora_inicio)}</strong>
        <span className="agenda-evento-data">{formatarDataCurta(evento.data_dia)}</span>
      </div>

      <div>
        <div className="agenda-evento-topo">
          <h3 className="agenda-evento-aluno">{evento.aluno}</h3>
          <span className={classeBadge(evento.status)}>{evento.status}</span>
        </div>

        <p className="agenda-evento-meta">Responsável: {evento.responsavel}</p>
        <p className="agenda-evento-meta">{evento.turma}</p>
        <p className="agenda-evento-meta">
          Solicitado por: {evento.solicitante?.nome_usuario}
        </p>

        {statusUpper === 'PENDENTE' && (
          <div className="agenda-evento-acoes">
            <button
              type="button"
              className="btn btn-sucesso"
              onClick={() => onConfirmar(evento.id_reuniao)}
            >
              Confirmar
            </button>
            <button
              type="button"
              className="btn btn-secundario"
              onClick={() => onRecusar(evento.id_reuniao)}
            >
              Recusar
            </button>
          </div>
        )}

        {statusUpper === 'CONFIRMADA' && (
          <div className="agenda-evento-acoes">
            <button
              type="button"
              className="btn btn-cyan"
              onClick={() => onFinalizar(evento.id_reuniao)}
            >
              Finalizar
            </button>
          </div>
        )}
      </div>
    </article>
  );
}
