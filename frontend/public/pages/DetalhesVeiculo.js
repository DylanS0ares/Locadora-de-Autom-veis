// src/pages/DetalhesVeiculo.js
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';

const DetalhesVeiculo = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [veiculo, setVeiculo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [reserva, setReserva] = useState({
    cliente_id: 1, // TODO: pegar do usuário logado
    data_inicio: '',
    data_fim: '',
    valor: 0,
  });

  useEffect(() => {
    const fetchVeiculo = async () => {
      try {
        const response = await api.get(`/veiculos/${id}`);
        setVeiculo(response.data);
      } catch (error) {
        console.error('Erro ao carregar veículo:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchVeiculo();
  }, [id]);

  const handleReserva = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/locacoes', {
        ...reserva,
        veiculo_id: parseInt(id),
      });
      alert('Reserva realizada com sucesso!');
      navigate('/minhas-reservas');
    } catch (error) {
      console.error('Erro ao criar reserva:', error);
      alert(error.response?.data?.detail || 'Erro ao criar reserva');
    }
  };

  if (loading) {
    return <div className="text-center py-20">Carregando...</div>;
  }

  if (!veiculo) {
    return <div className="text-center py-20">Veículo não encontrado</div>;
  }

  return (
    <div className="max-w-[1280px] mx-auto px-margin-desktop py-xl">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-xl">
        {/* Info do veículo */}
        <div className="bg-surface rounded-xl p-xl">
          <h1 className="font-display-lg text-display-lg text-on-surface">
            {veiculo.marca} {veiculo.modelo}
          </h1>
          <p className="text-on-surface-variant text-lg">Ano: {veiculo.ano}</p>
          <p className="text-on-surface-variant text-lg">Placa: {veiculo.placa}</p>
          <p className="text-on-surface-variant text-lg">
            Quilometragem: {veiculo.quilometragem} km
          </p>
          <span className={`inline-block mt-md px-md py-sm rounded-full ${
            veiculo.disponivel 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            {veiculo.disponivel ? '✅ Disponível para locação' : '❌ Indisponível'}
          </span>
        </div>

        {/* Formulário de reserva */}
        {veiculo.disponivel && (
          <div className="bg-surface rounded-xl p-xl">
            <h2 className="font-headline-lg text-headline-lg text-on-surface mb-md">
              Fazer Reserva
            </h2>
            <form onSubmit={handleReserva} className="flex flex-col gap-md">
              <div>
                <label className="font-label-sm text-label-sm text-on-surface-variant">
                  Data de Início
                </label>
                <input
                  type="datetime-local"
                  required
                  className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary"
                  value={reserva.data_inicio}
                  onChange={(e) => setReserva({ ...reserva, data_inicio: e.target.value })}
                />
              </div>
              <div>
                <label className="font-label-sm text-label-sm text-on-surface-variant">
                  Data de Fim
                </label>
                <input
                  type="datetime-local"
                  required
                  className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary"
                  value={reserva.data_fim}
                  onChange={(e) => setReserva({ ...reserva, data_fim: e.target.value })}
                />
              </div>
              <div>
                <label className="font-label-sm text-label-sm text-on-surface-variant">
                  Valor (R$)
                </label>
                <input
                  type="number"
                  required
                  min="0.01"
                  step="0.01"
                  className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary"
                  value={reserva.valor}
                  onChange={(e) => setReserva({ ...reserva, valor: parseFloat(e.target.value) })}
                />
              </div>
              <button
                type="submit"
                className="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-label-md text-label-md py-md px-xl rounded-lg transition-colors"
              >
                Confirmar Reserva
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default DetalhesVeiculo;