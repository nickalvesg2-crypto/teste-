import React from 'react';
import './layout.css';

export default function Header({
  nomeUsuario,
  onSair,
  menuAberto,
  onToggleMenu
}) {
  const inicial = (nomeUsuario || '?').trim().charAt(0).toUpperCase();

  return (
    <>
      <header className="header">
        <div className="header-esquerda">
          <button
            type="button"
            className="header-menu"
            aria-label="Abrir menu"
            aria-expanded={menuAberto}
            onClick={onToggleMenu}
          >
            ☰
          </button>
          <h1 className="header-titulo">AGENDA DA ORIENTAÇÃO</h1>
        </div>

        <div className="header-direita">
          <span className="header-usuario">{nomeUsuario}</span>
          <span className="header-avatar" aria-hidden="true">{inicial}</span>
          <button type="button" className="header-sair" onClick={onSair}>
            Sair
          </button>
        </div>
      </header>

      {menuAberto && (
        <div className="header-painel-mobile">
          <strong>{nomeUsuario}</strong>
          <button type="button" className="btn btn-ghost" onClick={onSair}>
            Sair
          </button>
        </div>
      )}
    </>
  );
}
