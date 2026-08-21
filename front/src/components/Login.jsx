import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import usuarioService from '../services/usuarioService';
import './Login.css';

export default function Login() {
  const { login } = useAuth();
  const [modoCadastro, setModoCadastro] = useState(false);

  const [nomeUsuario, setNomeUsuario] = useState('');
  const [senha, setSenha] = useState('');
  const [cargo, setCargo] = useState('SECRETARIA');
  const [erro, setErro] = useState('');
  const [carregando, setCarregando] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro('');
    setCarregando(true);

    try {
      if (modoCadastro) {
        await usuarioService.criar({
          nome_usuario: nomeUsuario,
          senha: senha,
          cargo: cargo
        });
        alert('Usuário cadastrado com sucesso! Faça login.');
        setModoCadastro(false);
      } else {
        const usuario = await usuarioService.login({ nome_usuario: nomeUsuario, senha });
        login(usuario);
      }
    } catch (err) {
      setErro(err.response?.data?.detail || 'Erro ao realizar operação.');
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="login-page">
      <form onSubmit={handleSubmit} className="login-card">
        <h2>{modoCadastro ? 'Criar Conta' : 'Login'}</h2>

        {erro && <div className="login-erro">{erro}</div>}

        <div className="login-campo">
          <label>Usuário</label>
          <input type="text" required value={nomeUsuario} onChange={(e) => setNomeUsuario(e.target.value)} />
        </div>

        <div className="login-campo">
          <label>Senha</label>
          <input type="password" required value={senha} onChange={(e) => setSenha(e.target.value)} />
        </div>

        {modoCadastro && (
          <div className="login-campo">
            <label>Cargo</label>
            <select value={cargo} onChange={(e) => setCargo(e.target.value)}>
              <option value="ADM">ADM</option>
              <option value="SECRETARIA">SECRETARIA</option>
              <option value="ORIENTADORA">ORIENTADORA</option>
              <option value="COORDENADORA">COORDENADORA</option>
              <option value="DIRETORA">DIRETORA</option>
            </select>
          </div>
        )}

        <button type="submit" disabled={carregando} className="btn btn-primario">
          {carregando ? 'Aguarde...' : modoCadastro ? 'Cadastrar' : 'Entrar'}
        </button>

        <p className="login-troca">
          {modoCadastro ? 'Já possui conta?' : 'Não tem uma conta?'}{' '}
          <span onClick={() => setModoCadastro(!modoCadastro)}>
            {modoCadastro ? 'Entrar' : 'Cadastre-se'}
          </span>
        </p>
      </form>
    </div>
  );
}
