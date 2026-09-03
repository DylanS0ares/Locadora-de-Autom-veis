// src/pages/Cadastro.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

const Cadastro = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ nome: '', email: '', senha: '' });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/usuarios/', form);
      alert('Cadastro realizado com sucesso! Faça login.');
      navigate('/login');
    } catch (error) {
      setError(error.response?.data?.detail || 'Erro ao cadastrar');
    }
  };

  return (
    <div className="max-w-md mx-auto px-margin-desktop py-xl">
      <div className="bg-surface rounded-xl p-xl shadow">
        <h1 className="font-headline-lg text-headline-lg text-on-surface text-center mb-lg">
          Criar Conta
        </h1>
        {error && (
          <div className="bg-red-100 text-red-800 p-sm rounded-lg mb-md">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="flex flex-col gap-md">
          <div>
            <label className="font-label-sm text-label-sm text-on-surface-variant">
              Nome
            </label>
            <input
              type="text"
              required
              className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary"
              value={form.nome}
              onChange={(e) => setForm({ ...form, nome: e.target.value })}
            />
          </div>
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
              Senha (mínimo 8 caracteres)
            </label>
            <input
              type="password"
              required
              minLength="8"
              className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary"
              value={form.senha}
              onChange={(e) => setForm({ ...form, senha: e.target.value })}
            />
          </div>
          <button
            type="submit"
            className="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-label-md text-label-md py-md px-xl rounded-lg transition-colors"
          >
            Cadastrar
          </button>
        </form>
        <p className="text-center mt-md text-on-surface-variant">
          Já tem conta? <Link to="/login" className="text-primary hover:underline">Faça login</Link>
        </p>
      </div>
    </div>
  );
};

export default Cadastro;