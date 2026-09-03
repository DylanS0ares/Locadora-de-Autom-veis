// src/pages/Catalogo.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const Catalogo = () => {
  const [veiculos, setVeiculos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVeiculos = async () => {
      try {
        const response = await api.get('/veiculos');
        setVeiculos(response.data);
      } catch (error) {
        console.error('Erro ao carregar catálogo:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchVeiculos();
  }, []);

  if (loading) {
    return <div className="text-center py-20">Carregando veículos...</div>;
  }

  return (
    <div className="max-w-[1280px] mx-auto px-margin-desktop py-xl">
      <h1 className="font-headline-lg text-headline-lg text-on-surface mb-lg">
        Nosso Catálogo
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-md">
        {veiculos.map((veiculo) => (
          <Link
            key={veiculo.id}
            to={`/veiculo/${veiculo.id}`}
            className="bg-surface rounded-xl overflow-hidden shadow hover:shadow-lg transition-shadow"
          >
            <div className="p-md">
              <h3 className="font-headline-md text-headline-md text-on-surface">
                {veiculo.marca} {veiculo.modelo}
              </h3>
              <p className="text-on-surface-variant">Ano: {veiculo.ano}</p>
              <p className="text-on-surface-variant">Placa: {veiculo.placa}</p>
              <span className={`inline-block mt-sm px-sm py-xs rounded-full text-sm ${
                veiculo.disponivel 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {veiculo.disponivel ? '✅ Disponível' : '❌ Indisponível'}
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Catalogo;