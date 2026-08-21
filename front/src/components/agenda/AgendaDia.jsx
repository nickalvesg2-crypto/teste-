import React from 'react';
import AgendaEvento from './AgendaEvento';
import './agenda.css';

export default function AgendaDia({
  titulo,
  eventos,
  carregando,
  onConfirmar,
  onRecusar,
  onFinalizar
}) {
  return (
    <section>
      <h2 className="agenda-dia-titulo">{titulo}</h2>

      {carregando ? (
        <p className="agenda-loading">Carregando agenda...</p>
      ) : eventos.length === 0 ? (
        <p className="agenda-vazia">Nenhum compromisso para hoje.</p>
      ) : (
        eventos.map((evento) => (
          <AgendaEvento
            key={evento.id_reuniao}
            evento={evento}
            onConfirmar={onConfirmar}
            onRecusar={onRecusar}
            onFinalizar={onFinalizar}
          />
        ))
      )}
    </section>
  );
}
