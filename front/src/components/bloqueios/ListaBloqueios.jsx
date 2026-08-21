import React from 'react';
import './ListaBloqueios.css';

function formatarData(valor) {
  if (!valor) return '—';

  const data = new Date(`${valor}T00:00:00`);
  if (Number.isNaN(data.getTime())) return String(valor);

  return data.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}

function formatarHora(valor) {
  if (!valor) return '—';
  return String(valor).slice(0, 5);
}

export default function ListaBloqueios({ bloqueios = [], onRemoverBloqueio = () => {} }) {
  if (!bloqueios || bloqueios.length === 0) {
    return (
      <section className="bloqueios-box">
        <div className="bloqueios-header">
          <h3>Horários bloqueados</h3>
        </div>
        <p className="bloqueios-vazio">Nenhum horário bloqueado no momento.</p>
      </section>
    );
  }

  return (
    <section className="bloqueios-box">
      <div className="bloqueios-header">
        <h3>Horários bloqueados</h3>
        <span className="bloqueios-badge">{bloqueios.length}</span>
      </div>

      <div className="bloqueios-lista">
        {bloqueios.map((bloqueio) => {
          const nomeUsuario =
            bloqueio.usuario?.nome_usuario ||
            bloqueio.nome_usuario ||
            'Usuário';

          const motivo = bloqueio.motivo || 'Sem motivo informado';
          const dataInicio = formatarData(bloqueio.data_dia || bloqueio.data_inicio);
          const dataFim = formatarData(bloqueio.data_fim || bloqueio.data_dia || bloqueio.data_inicio);
          const horaInicio = formatarHora(bloqueio.hora_inicio);
          const horaFim = formatarHora(bloqueio.hora_fim);

          return (
            <div className="bloqueio-item" key={bloqueio.id_bloqueio ?? `${nomeUsuario}-${dataInicio}-${horaInicio}`}>
              <div className="bloqueio-info">
                <strong>{nomeUsuario}</strong>
                <span>{motivo}</span>
                <small>
                  {dataInicio} • {horaInicio} às {horaFim}
                  {dataFim && dataFim !== dataInicio ? ` • até ${dataFim}` : ''}
                </small>
              </div>

              {bloqueio.id_bloqueio && (
                <button
                  type="button"
                  className="btn btn-ghost bloqueio-remover"
                  onClick={() => onRemoverBloqueio(bloqueio.id_bloqueio)}
                >
                  Remover
                </button>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
