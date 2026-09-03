// src/pages/MinhasReservas.js
import React, { useState, useEffect } from 'react';
import api from '../services/api';

const MinhasReservas = () => {
  const [reservas, setReservas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReservas = async () => {
      try {
        const response = await api.get('/locacoes');
        setReservas(response.data);
      } catch (error) {
        console.error('Erro ao carregar reservas:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchReservas();
  }, []);

  const handleDevolver = async (id) => {
    if (!window.confirm('Confirmar devolução do veículo?')) return;
    try {
      await api.post(`/locacoes/${id}/devolver`);
      alert('Veículo devolvido com sucesso!');
      // Recarregar lista
      const response = await api.get('/locacoes');
      setReservas(response.data);
    } catch (error) {
      console.error('Erro ao devolver:', error);
      alert(error.response?.data?.detail || 'Erro ao devolver veículo');
    }
  };

  if (loading) {
    return <div className="text-center py-20">Carregando reservas...</div>;
  }

  return (
    <div className="max-w-[1280px] mx-auto px-margin-desktop py-xl">
      <h1 className="font-headline-lg text-headline-lg text-on-surface mb-lg">
        Minhas Reservas
      </h1>
      {reservas.length === 0 ? (
        <p className="text-on-surface-variant">Nenhuma reserva encontrada.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-md">
          {reservas.map((reserva) => (
            <div key={reserva.id} className="bg-surface rounded-xl p-md shadow">
              <p><strong>Cliente ID:</strong> {reserva.cliente_id}</p>
              <p><strong>Veículo ID:</strong> {reserva.veiculo_id}</p>
              <p><strong>Início:</strong> {new Date(reserva.data_inicio).toLocaleString()}</p>
              <p><strong>Fim:</strong> {new Date(reserva.data_fim).toLocaleString()}</p>
              <p><strong>Valor:</strong> R$ {reserva.valor.toFixed(2)}</p>
              <button
                onClick={() => handleDevolver(reserva.id)}
                className="mt-sm bg-primary text-on-primary px-md py-sm rounded-lg hover:bg-primary-container transition-colors"
              >
                Devolver Veículo
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MinhasReservas;