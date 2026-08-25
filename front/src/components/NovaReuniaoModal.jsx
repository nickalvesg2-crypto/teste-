import React,  {useState, useEffect}  from 'react';
import reuniaoService from '../services/reuniaoService';
import usuarioService from '../services/usuarioService';

const extrairErro = (err) => {
  const detail = err?.response?.data?.detail;

  if (Array.isArray(detail)) {
    return detail.map((item) => item?.msg || item?.error || JSON.stringify(item)).join(' | ');
  }

  if (typeof detail === 'string') return detail;
  if (detail && typeof detail === 'object') return detail.msg || detail.error || JSON.stringify(detail);

  return err?.message || 'Erro ao agendar reunião.';
};

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
        // Filtra para não listar o próprio usuário logado como destinatário
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
    const payload = {
      aluno: formData.aluno,
      responsavel: formData.responsavel,
      turma: formData.turma,
      data_dia: formData.data,
      hora_inicio: formData.hora_inicio,
      hora_fim: formData.hora_fim,
      destinatario_id: formData.destinatario_id
        ? Number(formData.destinatario_id)
        : null
    };

    await reuniaoService.agendar(solicitanteId, payload);

    onSuccess();
    onClose();

  } catch (err) {
    setErro(extrairErro(err));
  } finally {
    setCarregando(false);
  }
};
  return (
    <div style={overlayStyle}>
      <div style={modalStyle}>
        <h3>Agendar Nova Reunião</h3>
        {erro && <div style={erroStyle}>{erro}</div>}

        <form onSubmit={handleSubmit}>
          <div style={inputGroupStyle}>
            <label>Aluno</label>
            <input type="text" name="aluno" required value={formData.aluno} onChange={handleChange} />
          </div>

          <div style={inputGroupStyle}>
            <label>Responsável</label>
            <input type="text" name="responsavel" required value={formData.responsavel} onChange={handleChange} />
          </div>

          <div style={inputGroupStyle}>
            <label>Turma</label>
            <input type="text" name="turma" required value={formData.turma} onChange={handleChange} />
          </div>

          <div style={inputGroupStyle}>
            <label>Data</label>
            <input type="date" name="data" required value={formData.data} onChange={handleChange} />
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <div style={{ ...inputGroupStyle, flex: 1 }}>
              <label>Hora Início</label>
              <input type="time" name="hora_inicio" required value={formData.hora_inicio} onChange={handleChange} />
            </div>

            <div style={{ ...inputGroupStyle, flex: 1 }}>
              <label>Hora Fim</label>
              <input type="time" name="hora_fim" required value={formData.hora_fim} onChange={handleChange} />
            </div>
          </div>

          <div style={inputGroupStyle}>
            <label>Destinatário</label>
            <select name="destinatario_id" value={formData.destinatario_id} onChange={handleChange}>
              <option value="">Selecione um destinatário (opcional)</option>
              {usuarios.map(u => (
                <option key={u.id_usuario} value={u.id_usuario}>{u.nome_usuario} ({u.cargo})</option>
              ))}
            </select>
          </div>

          <div style={botoesStyle}>
            <button type="button" onClick={onClose} style={btnCancelarStyle}>Cancelar</button>
            <button type="submit" disabled={carregando} style={btnSalvarStyle}>
              {carregando ? 'Salvando...' : 'Agendar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Estilos inline reaproveitáveis

const overlayStyle = { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 };
const modalStyle = { backgroundColor: '#fff', padding: '24px', borderRadius: '8px', width: '400px', maxHeight: '90vh', overflowY: 'auto' };
const inputGroupStyle = { marginBottom: '12px', display: 'flex', flexDirection: 'column' };
const botoesStyle = { display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '16px' };
const btnCancelarStyle = { padding: '8px 16px', backgroundColor: '#ccc', border: 'none', borderRadius: '4px', cursor: 'pointer' };
const btnSalvarStyle = { padding: '8px 16px', backgroundColor: '#2e7d32', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' };
const erroStyle = { backgroundColor: '#ffebee', color: '#c62828', padding: '8px', borderRadius: '4px', marginBottom: '12px' };