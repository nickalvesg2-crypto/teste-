import React from 'react';
import './layout.css';

function BadgeContador({ quantidade, tom }) {
  if (quantidade === undefined || quantidade === null) return null;

  return <span className={`aba-badge aba-badge-${tom}`}>{quantidade}</span>;
}

export default function Navegacao({
  abaAtiva = 'pendentes',
  onMudarAba = () => {},
  contadores = {
    pendentes: 0,
    confirmadas: 0,
    finalizadas: 0,
  },
  onAgendar = () => {},
  onBloquear = () => {},
}) {
  return (
    <div className="navegacao-wrap">
      <nav className="navegacao" aria-label="Abas da agenda">
        <button type="button" className="aba aba-agendar" onClick={onAgendar}>
          Agendar Reunião
        </button>

        <button
          type="button"
          className={`aba ${abaAtiva === 'pendentes' ? 'aba-ativa' : ''}`}
          onClick={() => onMudarAba('pendentes')}
        >
          Pendentes
          <BadgeContador quantidade={contadores.pendentes} tom="alerta" />
        </button>

        <button
          type="button"
          className={`aba ${abaAtiva === 'confirmadas' ? 'aba-ativa' : ''}`}
          onClick={() => onMudarAba('confirmadas')}
        >
          Confirmadas
          <BadgeContador quantidade={contadores.confirmadas} tom="sucesso" />
        </button>

        <button
          type="button"
          className={`aba ${abaAtiva === 'finalizadas' ? 'aba-ativa' : ''}`}
          onClick={() => onMudarAba('finalizadas')}
        >
          Finalizadas
          <BadgeContador quantidade={contadores.finalizadas} tom="neutro" />
        </button>
      </nav>

      <button
        type="button"
        className="btn btn-secundario btn-bloquear"
        onClick={onBloquear}
      >
        Bloquear agenda
      </button>
    </div>
  );
}
