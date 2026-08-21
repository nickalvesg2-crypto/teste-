import React, { useState, useEffect } from 'react';
import reuniaoService from '../../services/reuniaoService';
import usuarioService from '../../services/usuarioService';
import '../../styles/modal.css';

export default function NovaReuniaoModal({ solicitanteId, onClose, onSuccess }) {
  const [usuarios, setUsuarios] = useState([]);
  const [formData, setFormData] = useState({
    aluno: '',
    responsavel: '',
    turma: '',
    data: '',
    hora_inicio: '',
    hora_fim: '',
    destinatario_id: ''
  });
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState('');

  useEffect(() => {
    usuarioService.listar()
      .then(res => {
        const outrosUsuarios = res.filter(u => u.id_usuario !== solicitanteId);
        setUsuarios(outrosUsuarios);
      })
      .catch(() => setErro('Erro ao carregar lista de usuários.'));
  }, [solicitanteId]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setCarregando(true);
    setErro('');

    try {
      if (!formData.data || !formData.hora_inicio || !formData.hora_fim) {
        throw new Error('Data e horário da reunião são obrigatórios.');
      }

      if (formData.hora_fim <= formData.hora_inicio) {
        throw new Error('A hora de término deve ser maior que a hora de início.');
      }

      const payload = {
        aluno: formData.aluno,
        responsavel: formData.responsavel,
        turma: formData.turma,
        data_dia: formData.data,
        hora_inicio: formData.hora_inicio,
        hora_fim: formData.hora_fim,
        solicitado_por_id: solicitanteId,
        destinatario_id: formData.destinatario_id ? Number(formData.destinatario_id) : null,
      };

      await reuniaoService.agendar(solicitanteId, payload);
      onSuccess();
      onClose();
    } catch (err) {
      setErro(err.response?.data?.detail || err.message || 'Erro ao agendar reunião.');
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <h3>Agendar Nova Reunião</h3>
        {erro && <div className="modal-erro">{erro}</div>}

        <form onSubmit={handleSubmit}>
          <div className="modal-campo">
            <label>Aluno</label>
            <input type="text" name="aluno" required value={formData.aluno} onChange={handleChange} />
          </div>

          <div className="modal-campo">
            <label>Responsável</label>
            <input type="text" name="responsavel" required value={formData.responsavel} onChange={handleChange} />
          </div>

          <div className="modal-campo">
            <label>Turma</label>
            <input type="text" name="turma" required value={formData.turma} onChange={handleChange} />
          </div>

          <div className="modal-campo">
            <label>Data</label>
            <input type="date" name="data" required value={formData.data} onChange={handleChange} />
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
            <label>Destinatário</label>
            <select name="destinatario_id" value={formData.destinatario_id} onChange={handleChange}>
              <option value="">Selecione um destinatário (opcional)</option>
              {usuarios.map(u => (
                <option key={u.id_usuario} value={u.id_usuario}>{u.nome_usuario} ({u.cargo})</option>
              ))}
            </select>
          </div>

          <div className="modal-acoes">
            <button type="button" onClick={onClose} className="btn btn-ghost">Cancelar</button>
            <button type="submit" disabled={carregando} className="btn btn-primario">
              {carregando ? 'Salvando...' : 'Agendar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
