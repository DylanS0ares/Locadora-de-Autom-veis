// src/pages/Login.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

const Login = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', senha: '' });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await api.post('/usuarios/login', form);
      localStorage.setItem('access_token', response.data.access_token);
      navigate('/');
    } catch (error) {
      setError(error.response?.data?.detail || 'Erro ao fazer login');
    }
  };

  return (
    <div className="max-w-md mx-auto px-margin-desktop py-xl">
      <div className="bg-surface rounded-xl p-xl shadow">
        <h1 className="font-headline-lg text-headline-lg text-on-surface text-center mb-lg">
          Entrar
        </h1>
        {error && (
          <div className="bg-red-100 text-red-800 p-sm rounded-lg mb-md">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="flex flex-col gap-md">
          <div>
            <label className="font-label-sm text-label-sm text-on-surface-variant">
              E-mail
            </label>
            <input
              type="email"
              required
              className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </div>
          <div>
            <label className="font-label-sm text-label-sm text-on-surface-variant">
              Senha
            </label>
            <input
              type="password"
              required
              className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary"
              value={form.senha}
              onChange={(e) => setForm({ ...form, senha: e.target.value })}
            />
          </div>
          <button
            type="submit"
            className="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-label-md text-label-md py-md px-xl rounded-lg transition-colors"
          >
            Entrar
          </button>
        </form>
        <p className="text-center mt-md text-on-surface-variant">
          Não tem conta? <Link to="/cadastro" className="text-primary hover:underline">Cadastre-se</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;