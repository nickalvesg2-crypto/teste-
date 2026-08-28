import api from "./api";

const reuniaoService = {
listar: async () => {
  const { data } = await api.get("/reunioes/");
  return data;
},

agendar: async (solicitadoPorId, dados) => {
  const payload = {
    aluno: dados.aluno,
    responsavel: dados.responsavel,
    turma: dados.turma,
    data_dia: dados.data_dia,
    hora_inicio: dados.hora_inicio?.length === 5 ? `${dados.hora_inicio}:00` : dados.hora_inicio,
    hora_fim: dados.hora_fim?.length === 5 ? `${dados.hora_fim}:00` : dados.hora_fim,
    solicitado_por_id: Number(solicitadoPorId),
    destinatario_id: dados.destinatario_id ? Number(dados.destinatario_id) : null,
  };

  const { data } = await api.post("/reunioes", payload);
  return data;
},

confirmar: async (idReuniao, idUsuarioAcao) => {
  const { data } = await api.patch(
    `/reunioes/${idReuniao}/confirmar?id_usuario_acao=${idUsuarioAcao}`
  );
  return data;
},

recusar: async (idReuniao, idUsuarioAcao, motivo) => {
  const { data } = await api.patch(
    `/reunioes/${idReuniao}/recusar?id_usuario_acao=${idUsuarioAcao}`,
    { motivo }
  );
  return data;
},

reagendar: async (idReuniao, idUsuarioAcao, novaData, novaHoraInicio, novaHoraFim, motivo) => {
  const { data } = await api.patch(
    `/reunioes/${idReuniao}/reagendar?id_usuario_acao=${idUsuarioAcao}`,
    {
      nova_data: novaData,
      nova_hora_inicio: novaHoraInicio,
      nova_hora_fim: novaHoraFim,
      motivo,
    }
  );
  return data;
},

finalizar: async (idReuniao, idUsuarioAcao) => {
  const { data } = await api.patch(
    `/reunioes/${idReuniao}/finalizar?id_usuario_acao=${idUsuarioAcao}`
  );
  return data;
},

criarBloqueio: async (idUsuario, dados) => {
  const { data } = await api.post(
    `/reunioes/bloqueios?id_usuario=${idUsuario}`,
    dados
  );
  return data;
},

listarBloqueios: async (idUsuario) => {
  const { data } = await api.get(`/reunioes/bloqueios?id_usuario=${idUsuario}`);
  return data;
},

deletarBloqueio: async (idBloqueio, idUsuario) => {
  await api.delete(`/reunioes/bloqueios/${idBloqueio}?id_usuario=${idUsuario}`);
},
};

export default reuniaoService;