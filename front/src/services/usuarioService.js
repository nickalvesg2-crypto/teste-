import api from "./api";

const usuarioService = {
  criar: async (dados) => {
    const { data } = await api.post("/usuarios/", dados);
    return data;
  },

  login: async (dados) => {
    const { data } = await api.post("/usuarios/login", dados);
    return data;
  },

  listar: async () => {
    const { data } = await api.get("/usuarios/");
    return data;
  },

  buscarPorId: async (idUsuario) => {
    const { data } = await api.get(`/usuarios/${idUsuario}`);
    return data;
  },

  atualizar: async (idUsuario, dados) => {
    const { data } = await api.put(`/usuarios/${idUsuario}`, dados);
    return data;
  },

  deletar: async (idUsuario) => {
    await api.delete(`/usuarios/${idUsuario}`);
  },
};

export default usuarioService;
export { usuarioService };
