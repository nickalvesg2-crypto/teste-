import React from 'react';
import { formatarDataCurta, formatarHora } from '../../utils/data';
import './agenda.css';

function classeBadge(status) {
  if (status === 'Pendente') return 'badge badge-pendente';
  if (status === 'Confirmada') return 'badge badge-confirmada';
  if (status === 'Recusada') return 'badge badge-recusada';
  if (status === 'Finalizada') return 'badge badge-finalizada';
  if (status === 'Reagendamento Solicitado') return 'badge badge-reagendamento';
  return 'badge';
}

export default function AgendaEvento({
  evento,
  onConfirmar,
  onRecusar,
  onFinalizar
}) {
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

        {evento.status === 'Pendente' && (
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

        {evento.status === 'Confirmada' && (
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
