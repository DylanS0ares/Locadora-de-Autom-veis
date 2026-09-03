// src/pages/Home.js
import React, { useState, useEffect } from 'react';
import api from '../services/api';
import Hero from '../components/Hero';
import Categories from '../components/Categories';
import Offers from '../components/Offers';

const Home = () => {
  const [veiculos, setVeiculos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVeiculos = async () => {
      try {
        const response = await api.get('/veiculos/disponiveis');
        setVeiculos(response.data);
      } catch (error) {
        console.error('Erro ao carregar veículos:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchVeiculos();
  }, []);

  return (
    <>
      <Hero />
      <Categories veiculos={veiculos} loading={loading} />
      <Offers />
    </>
  );
};

export default Home;