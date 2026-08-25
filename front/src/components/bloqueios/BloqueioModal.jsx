import React, { useState } from 'react';
import reuniaoService from '../../services/reuniaoService';
import '../../styles/modal.css';

const extrairErro = (err) => {
  const detail = err?.response?.data?.detail;

  if (Array.isArray(detail)) {
    return detail.map((item) => item?.msg || item?.error || JSON.stringify(item)).join(' | ');
  }

  if (typeof detail === 'string') return detail;
  if (detail && typeof detail === 'object') return detail.msg || detail.error || JSON.stringify(detail);

  return err?.message || 'Erro ao criar bloqueio de agenda.';
};

export default function BloqueioModal({ usuarioId, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    data_dia: '',
    hora_inicio: '',
    hora_fim: '',
    motivo: ''
  });
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setCarregando(true);
    setErro('');

    try {
      await reuniaoService.criarBloqueio(usuarioId, formData);
      onSuccess();
      onClose();
    } catch (err) {
      setErro(extrairErro(err));
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <h3>Bloquear Horário na Agenda</h3>
        {erro && <div className="modal-erro">{erro}</div>}

        <form onSubmit={handleSubmit}>
          <div className="modal-campo">
            <label>Data</label>
            <input type="date" name="data_dia" required value={formData.data_dia} onChange={handleChange} />
          </div>

          <div className="modal-horarios">
            <div className="modal-campo">
              <label>Hora Início</label>
              <input type="time" name="hora_inicio" required value={formData.hora_inicio} onChange={handleChange} />
            </div>

            <div className="modal-campo">
              <label>Hora Fim</label>
              <input type="time" name="hora_fim" required value={formData.hora_fim} onChange={handleChange} />
            </div>
          </div>

          <div className="modal-campo">
            <label>Motivo</label>
            <textarea
              name="motivo"
              rows="3"
              required
              placeholder="Ex: Reunião pedagógica externa / Compromisso médico"
              value={formData.motivo}
              onChange={handleChange}
            />
          </div>

          <div className="modal-acoes">
            <button type="button" onClick={onClose} className="btn btn-ghost">Cancelar</button>
            <button type="submit" disabled={carregando} className="btn btn-secundario">
              {carregando ? 'Bloqueando...' : 'Confirmar Bloqueio'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
