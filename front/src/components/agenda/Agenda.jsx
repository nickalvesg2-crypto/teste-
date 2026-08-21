import React from 'react';
import AgendaDia from './AgendaDia';
import './agenda.css';

export default function Agenda({
  titulo,
  eventos,
  carregando,
  onConfirmar,
  onRecusar,
  onFinalizar
}) {
  return (
    <main className="agenda">
      <AgendaDia
        titulo={titulo}
        eventos={eventos}
        carregando={carregando}
        onConfirmar={onConfirmar}
        onRecusar={onRecusar}
        onFinalizar={onFinalizar}
      />
    </main>
  );
}
