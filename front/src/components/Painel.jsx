import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import reuniaoService from '../services/reuniaoService';
import Layout from './layout/Layout';
import Header from './layout/Header';
import Navegacao from './layout/Navegacao';
import Agenda from './agenda/Agenda';
import NovaReuniaoModal from './reunioes/NovaReuniaoModal';
import BloqueioModal from './bloqueios/BloqueioModal';
import ListaBloqueios from './bloqueios/ListaBloqueios';

const extrairErro = (err) => {
  const detail = err?.response?.data?.detail;

  if (Array.isArray(detail)) {
    return detail.map((item) => item?.msg || item?.error || JSON.stringify(item)).join(' | ');
  }

  if (typeof detail === 'string') return detail;
  if (detail && typeof detail === 'object') return detail.msg || detail.error || JSON.stringify(detail);

  return err?.message || 'Erro ao processar a ação.';
};

export default function Painel() {
  const { usuario: user, logout } = useAuth();

  const [reunioes, setReunioes] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [modalNovaReuniao, setModalNovaReuniao] = useState(false);
  const [modalBloqueio, setModalBloqueio] = useState(false);
  const [menuAberto, setMenuAberto] = useState(false);
  const [abaAtiva, setAbaAtiva] = useState('pendentes');
  const [bloqueios, setBloqueios] = useState([]);

  const normalizarStatus = (status) =>
    typeof status === 'string' ? status.trim().toLowerCase() : '';

  const contadores = {
    pendentes: reunioes.filter((reuniao) =>
      ['pendente', 'reagendamento solicitado'].includes(
        normalizarStatus(reuniao.status)
      )
    ).length,
    confirmadas: reunioes.filter(
      (reuniao) => normalizarStatus(reuniao.status) === 'confirmada'
    ).length,
    finalizadas: reunioes.filter(
      (reuniao) => normalizarStatus(reuniao.status) === 'finalizada'
    ).length,
  };

  const carregarReunioes = async () => {
    setCarregando(true);

    try {
      const res = await reuniaoService.listar();
      setReunioes(Array.isArray(res) ? res : res.data || []);
    } catch (err) {
      alert('Erro ao carregar reuniões.');
    } finally {
      setCarregando(false);
    }
  };

  const carregarBloqueios = async () => {
    if (!user?.id_usuario) {
      setBloqueios([]);
      return;
    }

    try {
      const resposta = await reuniaoService.listarBloqueios(user.id_usuario);
      setBloqueios(Array.isArray(resposta) ? resposta : resposta.data || []);
    } catch (err) {
      console.error('Erro ao carregar bloqueios.', err);
      setBloqueios([]);
    }
  };

  useEffect(() => {
    carregarReunioes();
    carregarBloqueios();
  }, []);

  useEffect(() => {
    if (user?.id_usuario) {
      carregarBloqueios();
    }
  }, [user?.id_usuario]);

  const eventosFiltrados = reunioes
    .filter((reuniao) => {
      const status = normalizarStatus(reuniao.status);

      if (abaAtiva === 'pendentes') {
        return ['pendente', 'reagendamento solicitado'].includes(status);
      }

      if (abaAtiva === 'confirmadas') {
        return status === 'confirmada';
      }

      if (abaAtiva === 'finalizadas') {
        return status === 'finalizada';
      }

      return false;
    })
    .slice()
    .sort((a, b) => {
      const dataCompare = String(a.data_dia).localeCompare(String(b.data_dia));
      if (dataCompare !== 0) return dataCompare;
      return String(a.hora_inicio).localeCompare(String(b.hora_inicio));
    });

  const tituloAgenda = {
    pendentes: 'Pendentes',
    confirmadas: 'Confirmadas',
    finalizadas: 'Finalizadas',
  }[abaAtiva] || 'Pendentes';

  const handleConfirmar = async (idReuniao) => {
    try {
      await reuniaoService.confirmar(idReuniao, user?.id_usuario);
      carregarReunioes();
    } catch (err) {
      alert(extrairErro(err) || 'Erro ao confirmar reunião.');
    }
  };

  const handleRecusar = async (idReuniao) => {
    const motivo = prompt('Digite o motivo da recusa (opcional):');

    if (motivo !== null) {
      try {
        await reuniaoService.recusar(idReuniao, user?.id_usuario, motivo);
        carregarReunioes();
      } catch (err) {
        alert(extrairErro(err) || 'Erro ao recusar reunião.');
      }
    }
  };

  const handleFinalizar = async (idReuniao) => {
    if (window.confirm('Deseja marcar esta reunião como finalizada?')) {
      try {
        await reuniaoService.finalizar(idReuniao, user?.id_usuario);
        carregarReunioes();
      } catch (err) {
        alert(extrairErro(err) || 'Erro ao finalizar reunião.');
      }
    }
  };

  const handleRemoverBloqueio = async (idBloqueio) => {
    if (!user?.id_usuario) return;

    try {
      await reuniaoService.deletarBloqueio(idBloqueio, user.id_usuario);
      await carregarBloqueios();
    } catch (err) {
      alert(extrairErro(err) || 'Erro ao remover bloqueio.');
    }
  };

  return (
    <Layout>
      <Header
        nomeUsuario={user?.nome_usuario}
        onSair={logout}
        menuAberto={menuAberto}
        onToggleMenu={() => setMenuAberto((aberto) => !aberto)}
      />

      <Navegacao
        abaAtiva={abaAtiva}
        onMudarAba={setAbaAtiva}
        contadores={contadores}
        onAgendar={() => setModalNovaReuniao(true)}
        onBloquear={() => setModalBloqueio(true)}
      />

      <Agenda
        titulo={tituloAgenda}
        eventos={eventosFiltrados}
        carregando={carregando}
        onConfirmar={handleConfirmar}
        onRecusar={handleRecusar}
        onFinalizar={handleFinalizar}
      />

      <ListaBloqueios
        bloqueios={bloqueios}
        onRemoverBloqueio={handleRemoverBloqueio}
      />

      {modalNovaReuniao && (
        <NovaReuniaoModal
          solicitanteId={user?.id_usuario}
          onClose={() => setModalNovaReuniao(false)}
          onSuccess={() => {
            carregarReunioes();
            carregarBloqueios();
          }}
        />
      )}

      {modalBloqueio && (
        <BloqueioModal
          usuarioId={user?.id_usuario}
          onClose={() => setModalBloqueio(false)}
          onSuccess={() => {
            carregarReunioes();
            carregarBloqueios();
          }}
        />
      )}
    </Layout>
  );
}
