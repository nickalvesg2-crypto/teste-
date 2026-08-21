import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

function recuperarUsuario() {
  try {
    const dadosSalvos = localStorage.getItem("usuario");
    return dadosSalvos ? JSON.parse(dadosSalvos) : null;
  } catch {
    localStorage.removeItem("usuario");
    return null;
  }
}

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(recuperarUsuario);

  function login(dadosUsuario) {
    const usuarioLogado = {
      id_usuario: dadosUsuario.id_usuario,
      nome_usuario: dadosUsuario.nome_usuario,
      cargo: dadosUsuario.cargo,
    };

    setUsuario(usuarioLogado);
    localStorage.setItem("usuario", JSON.stringify(usuarioLogado));
  }

  function logout() {
    setUsuario(null);
    localStorage.removeItem("usuario");
  }

  return (
    <AuthContext.Provider value={{ usuario, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth deve ser usado dentro de AuthProvider.");
  }

  return context;
}
