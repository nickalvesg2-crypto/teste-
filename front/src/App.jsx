import React from 'react';
import { useAuth } from './context/AuthContext';
import Login from './components/Login';
import Painel from './components/Painel';

export default function App() {
  const { usuario } = useAuth(); // Usando 'usuario' conforme exportado pelo AuthContext

  return usuario ? <Painel /> : <Login />;
}