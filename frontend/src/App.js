// src/App.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

// ---------- Configuração da API ----------
const api = axios.create({
  baseURL: 'https://locadora-backend.onrender.com',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ---------- Contexto de Autenticação ----------
const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = async (email, senha) => {
    try {
      const response = await api.post('/usuarios/login', { email, senha });
      localStorage.setItem('access_token', response.data.access_token);
      setUser({ email });
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.detail || 'Erro no login' };
    }
  };

  const cadastro = async (nome, email, senha) => {
    try {
      await api.post('/usuarios/', { nome, email, senha });
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.detail || 'Erro no cadastro' };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, cadastro, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => useContext(AuthContext);

// ---------- Componentes ----------
const Header = () => {
  const { user, logout } = useAuth();
  return (
    <header className="fixed top-0 w-full z-50 bg-surface/80 backdrop-blur-xl shadow-[0_4px_15px_rgba(0,53,39,0.04)]">
      <div className="h-20 max-w-[1280px] mx-auto px-margin-desktop flex items-center justify-between gap-md">
        <div className="flex items-center gap-base">
          <img alt="Green Mobi Locadora" className="h-8 w-auto object-contain" src="/images/logo.png" />
          <span className="font-headline-md text-headline-md text-primary tracking-tight">Green Mobi</span>
        </div>
        <nav className="hidden md:flex items-center gap-lg">
          <Link to="/" className="text-primary font-bold transition-colors">Início</Link>
          <Link to="/catalogo" className="font-label-md text-label-md text-on-surface-variant hover:text-primary transition-colors">Catálogo</Link>
          <Link to="/minhas-reservas" className="font-label-md text-label-md text-on-surface-variant hover:text-primary transition-colors">Minhas Reservas</Link>
          {user ? (
            <button onClick={logout} className="font-label-md text-label-md text-red-600 hover:text-red-800">Sair</button>
          ) : (
            <Link to="/login" className="font-label-md text-label-md text-primary hover:text-primary-container transition-colors">Entrar</Link>
          )}
        </nav>
        <div className="flex items-center gap-md">
          <button className="p-xs text-on-surface-variant hover:text-primary transition-colors">
            <span className="material-symbols-outlined">search</span>
          </button>
          <div className="flex items-center gap-sm bg-surface-container-low py-xs px-sm rounded-full cursor-pointer hover:bg-surface-container-high transition-colors">
            <img alt="Perfil" className="w-8 h-8 rounded-full object-cover" src="https://lh3.googleusercontent.com/aida/AEtjO1X7G5A2X-kjiq0UIBMzpiaiGTJwp4KXN0Ab6MJ7vyCzx-m1cmfC-1Z_wmJgfRWY7HdSInwkN60dkRc2fugR5HjoRBH42shTaVXEFBblCT_o0kDYmidrkj5fqaECucCnx4muC7pM86LapZX4mhn9gVX_dbwr1TAPNJPChj2hUB49UiHrZGWcotPdLHJ_N4jaUYdfPhu5U3loGkulb1wtOchV_aWYN28Mby_Yhdl5bZaCZszx_7vcvZMsIqs" />
            <span className="hidden lg:block font-label-md text-label-md text-on-surface">Minha Conta</span>
          </div>
        </div>
      </div>
    </header>
  );
};

const Hero = () => (
  <div className="relative w-full h-[600px] flex items-center justify-center -mt-20 overflow-hidden">
    <div className="absolute inset-0 z-0">
      <div className="w-full h-full bg-cover bg-center" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuDVsDKUKSPaivFlIaldwwqMZu_4N506RLr8_LXZqaW5Obc7_rR137BQ_knBn_mJmc_GDQVNiz5AYkTcdQJbQp_AHtodBpn7SjTTnY18si0cE2GrL26ZzzVq1mrt4j3ScQ2wrcCa5kjRoLnRA8PdcjCSw6jVMEA28ZscRrIhaf6pkQ8owwk9I27plsbs6rImYD-tHnqbq0bw8ea_i9D_j2IQAxSKB5QShJ7bNQVqLvNQywNQiMP15M7b')" }} />
      <div className="absolute inset-0 bg-gradient-to-t from-background via-background/40 to-transparent" />
      <div className="absolute inset-0 bg-primary/20 mix-blend-multiply" />
    </div>
    <div className="relative z-10 max-w-[1280px] w-full px-margin-desktop mt-20 flex flex-col items-start">
      <span className="font-label-sm text-label-sm text-secondary-container tracking-[0.2em] uppercase mb-sm">Descubra o Novo Padrão</span>
      <h1 className="font-display-lg text-display-lg text-on-primary max-w-2xl mb-md drop-shadow-lg">Redefina sua Jornada com Luxo e Conforto</h1>
      <p className="font-body-lg text-body-lg text-surface-container-highest max-w-xl mb-xl drop-shadow-md">Descubra uma frota selecionada de veículos premium, projetados para o viajante exigente. Desempenho incomparável, conforto absoluto.</p>
      <div className="w-full max-w-4xl bg-surface/95 backdrop-blur-md rounded-xl p-md shadow-[0_10px_30px_rgba(0,53,39,0.08)] flex flex-col md:flex-row items-center gap-sm">
        <div className="flex-1 w-full flex items-center bg-surface-container-low rounded-lg px-md py-sm focus-within:bg-surface-container group">
          <span className="material-symbols-outlined text-outline group-focus-within:text-primary mr-sm">location_on</span>
          <div className="flex flex-col w-full">
            <label className="font-label-sm text-label-sm text-on-surface-variant">Local de Retirada</label>
            <input className="bg-transparent border-none outline-none font-body-md text-body-md text-on-surface w-full" placeholder="Cidade, Aeroporto ou Endereço" type="text" />
          </div>
        </div>
        <div className="w-px h-10 bg-outline-variant/30 hidden md:block" />
        <div className="flex-1 w-full flex items-center bg-surface-container-low rounded-lg px-md py-sm focus-within:bg-surface-container group">
          <span className="material-symbols-outlined text-outline group-focus-within:text-primary mr-sm">calendar_month</span>
          <div className="flex flex-col w-full">
            <label className="font-label-sm text-label-sm text-on-surface-variant">Datas</label>
            <input className="bg-transparent border-none outline-none font-body-md text-body-md text-on-surface w-full cursor-pointer" placeholder="Selecione as datas" type="text" />
          </div>
        </div>
        <button className="w-full md:w-auto bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-label-md text-label-md py-md px-xl rounded-lg flex items-center justify-center gap-sm group">
          <span>Buscar Frota</span>
          <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform">arrow_forward</span>
        </button>
      </div>
    </div>
  </div>
);

const Categories = () => {
  const categories = [
    { title: 'Compacto Urbano', label: 'Compacto', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCE7R68mAfBRbXgrQGPm0CMbEnlWWuUL1SGUFEDFIFLZWQa4DgenOvZzEyNYO4axMSEY1ATK6dLR8FjlVfOSWTZH6_YVHfBrMXMsEiAH1hF2ke9zed_81Z5k9ypDo2CCECY2cOjNn8WaP7kls1SbRTWMJNhivxfO5EeahRmj5Cv_57TBmsgDmL-_x7j-V0vpmflof1N_1UeON8QeADZlKZJ4-k4KqGDU2AjT70GUqL2OXFaWaAkpM-N' },
    { title: 'Sedan Executivo', label: 'Sedan', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAwB0dhLH4DIQwqCFyU_V_JIZvcZrwK1J_z8Xuq5bkJ4r2zNRXk8OBKJ6SIniuzD5LBSIFoD-F75rkYV8jKtxEFaC7ykRNzY4bElSB_D7bYHnggda0XcacpKqvuwxzpuCcIrNwF0nB5nSXMtYWALwYnJ674xvirP8QYFaWVu45DYJIOLVGD-aRS9CJUnItbpjSyLpiAuUjHDAM39Frw7Yi-cgCzEI3iVhOFJXbGKs2Ufs_S0hKXC3dz' },
    { title: 'Esportivo de Luxo', label: 'Esportivo', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCJOwFiCiJkJEuTlnNHnqyjUz3Q1VWiZQz2rfAevv39tjUFG0-TPAkx5fOBxoX_pTPpqrQaTp76tWRiC4nq94HXbcLud-vXuP-0epv76lh0p4viNZTSJcbyEOG0tkQhUbbMrL3AtYztOUwwYsg652E83BJvudfDNatFYYhXK816CrTpq7jF0chU5YbK9NqRswrZTFAhJN4BGbOtNIQhES72JjoZmTynf8osB39nWi5RfxTlCGEekmwl', extra: 'lg:-translate-y-8' },
    { title: 'SUV Familiar', label: 'SUV', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA5YlTfuYUjbz8aeXmAkhrRXrB5SI9GfPc4DJhoswS1Zc6bu5iT4lkAwI-IkzNEVDfHfymGFwit6MsmSZzQ-8gVBYzAFig95AUZ0TZvBXoxMLpGNKS7GH-Jk6EXwB3EPyZDpl71kV9wngWQjdc13bOeBofZaX3DMrKQCUAB8-gFChP5omEGDaJFVPTM3BsENBty38-bwbIhSD2PH9dMXmJ2I4UxvepClu4mSkhXRyMcj4_RVc0-t4tm' },
  ];
  return (
    <div className="max-w-[1280px] w-full mx-auto px-margin-desktop py-xl">
      <div className="flex items-end justify-between mb-lg">
        <div><h2 className="font-headline-lg text-headline-lg text-on-surface mb-xs">Explore por Categoria</h2><p className="font-body-md text-body-md text-on-surface-variant">Encontre o veículo perfeito para sua próxima aventura.</p></div>
        <Link to="/catalogo" className="hidden md:flex items-center gap-xs font-label-md text-label-md text-primary hover:text-primary-container transition-colors group">Ver Todas as Categorias <span className="material-symbols-outlined text-[18px] group-hover:translate-x-1 transition-transform">east</span></Link>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-md">
        {categories.map((cat, idx) => (
          <Link key={idx} to="/catalogo" className={`group relative rounded-xl overflow-hidden aspect-[4/5] bg-surface-container flex flex-col justify-end p-md transition-transform hover:-translate-y-2 duration-300 ${cat.extra || ''}`}>
            <div className="absolute inset-0"><div className="w-full h-full bg-cover bg-center transition-transform duration-700 group-hover:scale-105" style={{ backgroundImage: `url('${cat.img}')` }} /><div className="absolute inset-0 bg-gradient-to-t from-primary/90 via-primary/20 to-transparent" /></div>
            <div className="relative z-10"><span className="font-label-sm text-label-sm text-secondary-container uppercase tracking-wider mb-xs block">{cat.label}</span><h3 className="font-headline-md text-headline-md text-on-primary">{cat.title}</h3></div>
          </Link>
        ))}
      </div>
    </div>
  );
};

const Offers = () => (
  <div className="w-full bg-surface-container-lowest py-xl relative overflow-hidden">
    <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-secondary-container/20 rounded-full blur-[100px] -translate-y-1/2 translate-x-1/4 pointer-events-none" />
    <div className="max-w-[1280px] w-full mx-auto px-margin-desktop relative z-10">
      <div className="flex flex-col items-center text-center mb-lg">
        <span className="font-label-sm text-label-sm text-primary uppercase tracking-[0.1em] mb-sm bg-primary/5 px-sm py-xs rounded-full">Oferta por Tempo Limitado</span>
        <h2 className="font-headline-lg text-headline-lg text-on-surface mb-xs">Ofertas Exclusivas</h2>
        <p className="font-body-md text-body-md text-on-surface-variant max-w-2xl">Aproveite nossas promoções atuais e alugue com ainda mais vantagens.</p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-md">
        <div className="bg-surface rounded-2xl overflow-hidden shadow-[0_8px_24px_rgba(0,53,39,0.04)] flex flex-col md:flex-row group transition-all hover:shadow-[0_12px_32px_rgba(0,53,39,0.08)]">
          <div className="w-full md:w-2/5 h-48 md:h-auto relative"><div className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-105" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuDa_dfHV48ZSKpSnGskKjnzx_5N5Ya-O4isDcf6pGTLF330lKFgQ3AavpoF8axVCWEv6iHLxO9nk8br3OmIL4ndmx9s6bLfHDz1F5YJPQ8t4AQloDMKm0MEzvPxuDOZQeLHG16odw4dfCcaLlWHNmu4Igev91e9uI66dhp-IBNZNH95ntarAzNc2Rju5Ft-5gwir6bTygJ6sqfALgBJ-Uaiex335gQ7GFEgi5WBwTVM5NKO9OoWCsOy')" }} /></div>
          <div className="w-full md:w-3/5 p-md flex flex-col justify-between">
            <div><div className="flex items-center gap-sm mb-sm"><span className="material-symbols-outlined text-primary">local_offer</span><span className="font-label-sm text-label-sm text-primary">Fim de Semana</span></div><h3 className="font-headline-md text-headline-md text-on-surface mb-xs">20% Off em Locação de Fim de Semana</h3><p className="font-body-md text-body-md text-on-surface-variant line-clamp-2 mb-md">Alugue qualquer veículo da nossa frota premium para o fim de semana e aproveite grandes economias.</p></div>
            <div className="flex items-center justify-between mt-auto"><span className="font-label-sm text-label-sm text-outline">Código: WKND20</span><button className="text-primary font-label-md text-label-md hover:text-primary-container transition-colors flex items-center gap-xs">Resgatar Oferta <span className="material-symbols-outlined text-[18px]">arrow_forward</span></button></div>
          </div>
        </div>
        <div className="bg-primary rounded-2xl overflow-hidden shadow-[0_8px_24px_rgba(0,53,39,0.1)] flex flex-col md:flex-row group transition-all hover:shadow-[0_12px_32px_rgba(0,53,39,0.15)] relative">
          <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_2px_2px,_#ffffff_1px,_transparent_0)] [background-size:24px_24px] pointer-events-none" />
          <div className="w-full md:w-2/5 h-48 md:h-auto relative z-10"><div className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-105 mix-blend-luminosity opacity-80" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuD931NScW80lppSMm7A61IcfxpPKh-JrD-GJFncEUiO4bhMZ8lIORVO7biC9X3p7-5EblvkUQrQYbkYIhJjWDJyI9zkVGqukvJpqlb40g1jLqQWnPhCzhMkZpRxN2jgvEJyeM03fTJ0VsUApnJ9ExUHK2sIOtAa7jYTIU-Lo3hp6qdBpR6rAL-ObGxDVBOIfUlmj_RaLpvJxg_2izr3elIABt2VQOlqHDXOFlaQWdKElQkQ0AdcG0fu')" }} /></div>
          <div className="w-full md:w-3/5 p-md flex flex-col justify-between relative z-10">
            <div><div className="flex items-center gap-sm mb-sm"><span className="material-symbols-outlined text-secondary-container">workspace_premium</span><span className="font-label-sm text-label-sm text-secondary-container">Primeira Locação</span></div><h3 className="font-headline-md text-headline-md text-on-primary mb-xs">Upgrade Gratuito</h3><p className="font-body-md text-body-md text-surface-container-highest line-clamp-2 mb-md">Reserve um veículo da categoria padrão e ganhe um upgrade para a categoria premium.</p></div>
            <div className="flex items-center justify-between mt-auto"><span className="font-label-sm text-label-sm text-surface-variant">Código: UPGRADE1</span><button className="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-label-md text-label-md py-sm px-md rounded-lg transition-colors">Reservar Agora</button></div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

const Footer = () => (
  <footer className="w-full bg-surface-container-lowest py-xl border-t border-outline-variant/30">
    <div className="max-w-[1280px] mx-auto px-margin-desktop">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-lg mb-lg">
        <div className="col-span-1 md:col-span-1">
          <div className="flex items-center gap-base mb-md"><img alt="Green Mobi Locadora" className="h-6 w-auto object-contain" src="/images/logo.png" /><span className="font-headline-md text-label-md text-primary">Green Mobi</span></div>
          <p className="font-body-md text-on-surface-variant opacity-80 leading-relaxed">Locação de veículos premium com excelência e conforto. Redefina sua experiência na estrada.</p>
        </div>
        <div className="flex flex-col gap-sm"><h4 className="font-label-md text-label-md text-on-surface uppercase tracking-wider mb-base">Empresa</h4><Link to="#" className="font-body-md text-on-surface-variant hover:text-primary">Nossa História</Link><Link to="#" className="font-body-md text-on-surface-variant hover:text-primary">Carreiras</Link><Link to="#" className="font-body-md text-on-surface-variant hover:text-primary">Política de Qualidade</Link></div>
        <div className="flex flex-col gap-sm"><h4 className="font-label-md text-label-md text-on-surface uppercase tracking-wider mb-base">Suporte</h4><Link to="#" className="font-body-md text-on-surface-variant hover:text-primary">Central de Ajuda</Link><Link to="#" className="font-body-md text-on-surface-variant hover:text-primary">Termos de Serviço</Link><Link to="#" className="font-body-md text-on-surface-variant hover:text-primary">Política de Privacidade</Link></div>
        <div className="flex flex-col gap-sm"><h4 className="font-label-md text-label-md text-on-surface uppercase tracking-wider mb-base">Conecte-se</h4><div className="flex gap-md text-on-surface-variant"><span className="material-symbols-outlined cursor-pointer hover:text-primary">public</span><span className="material-symbols-outlined cursor-pointer hover:text-primary">mail</span><span className="material-symbols-outlined cursor-pointer hover:text-primary">share</span></div></div>
      </div>
      <div className="pt-md border-t border-outline-variant/20 flex flex-col md:flex-row justify-between items-center gap-sm"><p className="font-label-sm text-label-sm text-on-surface-variant">© 2026 Green Mobi Locadora. Todos os direitos reservados.</p><div className="flex gap-md"><span className="font-label-sm text-label-sm text-on-surface-variant">Excelência em locação de veículos</span></div></div>
    </div>
  </footer>
);

// ---------- Páginas ----------
const Home = () => (
  <>
    <Hero />
    <Categories />
    <Offers />
  </>
);

const Catalogo = () => {
  const [veiculos, setVeiculos] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    api.get('/veiculos')
      .then(res => { setVeiculos(res.data); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  }, []);
  if (loading) return <div className="text-center py-20">Carregando veículos...</div>;
  return (
    <div className="max-w-[1280px] mx-auto px-margin-desktop py-xl">
      <h1 className="font-headline-lg text-headline-lg text-on-surface mb-lg">Nosso Catálogo</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-md">
        {veiculos.map(v => (
          <Link key={v.id} to={`/veiculo/${v.id}`} className="bg-surface rounded-xl overflow-hidden shadow hover:shadow-lg transition-shadow p-md">
            <h3 className="font-headline-md text-headline-md text-on-surface">{v.marca} {v.modelo}</h3>
            <p className="text-on-surface-variant">Ano: {v.ano}</p>
            <p className="text-on-surface-variant">Placa: {v.placa}</p>
            <span className={`inline-block mt-sm px-sm py-xs rounded-full text-sm ${v.disponivel ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>{v.disponivel ? '✅ Disponível' : '❌ Indisponível'}</span>
          </Link>
        ))}
      </div>
    </div>
  );
};

const DetalhesVeiculo = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [veiculo, setVeiculo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [reserva, setReserva] = useState({ data_inicio: '', data_fim: '', valor: 0 });

  useEffect(() => {
    api.get(`/veiculos/${id}`).then(res => { setVeiculo(res.data); setLoading(false); }).catch(() => setLoading(false));
  }, [id]);

  const handleReserva = async (e) => {
    e.preventDefault();
    if (!user) { alert('Faça login para reservar'); return navigate('/login'); }
    try {
      await api.post('/locacoes', { ...reserva, veiculo_id: parseInt(id), cliente_id: 1 });
      alert('Reserva realizada!');
      navigate('/minhas-reservas');
    } catch (error) {
      alert(error.response?.data?.detail || 'Erro na reserva');
    }
  };

  if (loading) return <div className="text-center py-20">Carregando...</div>;
  if (!veiculo) return <div className="text-center py-20">Veículo não encontrado</div>;

  return (
    <div className="max-w-[1280px] mx-auto px-margin-desktop py-xl">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-xl">
        <div className="bg-surface rounded-xl p-xl">
          <h1 className="font-display-lg text-display-lg text-on-surface">{veiculo.marca} {veiculo.modelo}</h1>
          <p className="text-on-surface-variant text-lg">Ano: {veiculo.ano}</p>
          <p className="text-on-surface-variant text-lg">Placa: {veiculo.placa}</p>
          <p className="text-on-surface-variant text-lg">Quilometragem: {veiculo.quilometragem} km</p>
          <span className={`inline-block mt-md px-md py-sm rounded-full ${veiculo.disponivel ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>{veiculo.disponivel ? '✅ Disponível' : '❌ Indisponível'}</span>
        </div>
        {veiculo.disponivel && (
          <div className="bg-surface rounded-xl p-xl">
            <h2 className="font-headline-lg text-headline-lg text-on-surface mb-md">Fazer Reserva</h2>
            <form onSubmit={handleReserva} className="flex flex-col gap-md">
              <div><label className="font-label-sm text-label-sm text-on-surface-variant">Data de Início</label><input type="datetime-local" required className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary" value={reserva.data_inicio} onChange={e => setReserva({ ...reserva, data_inicio: e.target.value })} /></div>
              <div><label className="font-label-sm text-label-sm text-on-surface-variant">Data de Fim</label><input type="datetime-local" required className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary" value={reserva.data_fim} onChange={e => setReserva({ ...reserva, data_fim: e.target.value })} /></div>
              <div><label className="font-label-sm text-label-sm text-on-surface-variant">Valor (R$)</label><input type="number" required min="0.01" step="0.01" className="w-full bg-surface-container-low rounded-lg px-md py-sm outline-none focus:ring-2 focus:ring-primary" value={reserva.valor} onChange={e => setReserva({ ...reserva, valor: parseFloat(e.target.value) })} /></div>
              <button type="submit" className="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-label-md text-label-md py-md px-xl rounded-lg transition-colors">Confirmar Reserva</button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

const MinhasReservas = () => {
  const [reservas, setReservas] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    api.get('/locacoes').then(res => { setReservas(res.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);
  const devolver = async (id) => {
    if (!window.confirm('Devolver veículo?')) return;
    try { await api.post(`/locacoes/${id}/devolver`); alert('Devolvido!'); setReservas(reservas.filter(r => r.id !== id)); } catch (e) { alert('Erro ao devolver'); }
  };
  if (loading) return <div className="text-center py-20">Carregando reservas...</div>;
  return (
    <div className="max-w-[1280px] mx-auto px-margin-desktop py-xl">
      <h1 className="font-headline-lg text-headline-lg text-on-surface mb-lg">Minhas Reservas</h1>
      {reservas.length === 0 ? <p className="text-on-surface-variant">Nenhuma reserva encontrada.</p> : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-md">
          {reservas.map(r => (
            <div key={r.id} className="bg-surface rounded-xl p-md shadow">
              <p><strong>Veículo:</strong> {r.veiculo_id}</p>
              <p><strong>Início:</strong> {new Date(r.data_inicio).toLocaleString()}</p>
              <p><strong>Fim:</strong> {new Date(r.data_fim).toLocaleString()}</p>
              <p><strong>Valor:</strong> R$ {r.valor.toFixed(2)}</p>
              <button onClick={() => devolver(r.id)} className="mt-sm bg-primary text-on-primary px-md py-sm rounded-lg hover:bg-primary-container transition-colors">Devolver</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: '', senha: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    const result = await login(form.email, form.senha);
    if (result.success) navigate('/');
    else setError(result.message);
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <div className="bg-surface rounded-xl p-8 shadow-lg">
        <h1 className="text-3xl font-bold text-on-surface text-center mb-6">Entrar</h1>
        {error && <div className="bg-red-100 text-red-800 p-3 rounded-lg mb-4">{error}</div>}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div><label className="text-sm font-medium text-on-surface-variant">E-mail</label><input type="email" required className="w-full bg-surface-container-low rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-primary" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} /></div>
          <div><label className="text-sm font-medium text-on-surface-variant">Senha</label><input type="password" required className="w-full bg-surface-container-low rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-primary" value={form.senha} onChange={e => setForm({ ...form, senha: e.target.value })} /></div>
          <button type="submit" disabled={loading} className="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-medium py-3 px-6 rounded-lg transition-colors disabled:opacity-50">{loading ? 'Entrando...' : 'Entrar'}</button>
        </form>
        <p className="text-center mt-4 text-on-surface-variant">Não tem conta? <Link to="/cadastro" className="text-primary hover:underline">Cadastre-se</Link></p>
      </div>
    </div>
  );
};

const Cadastro = () => {
  const navigate = useNavigate();
  const { cadastro } = useAuth();
  const [form, setForm] = useState({ nome: '', email: '', senha: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    const result = await cadastro(form.nome, form.email, form.senha);
    if (result.success) {
      alert('Cadastro realizado com sucesso! Faça login.');
      navigate('/login');
    } else {
      setError(result.message);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <div className="bg-surface rounded-xl p-8 shadow-lg">
        <h1 className="text-3xl font-bold text-on-surface text-center mb-6">Criar Conta</h1>
        {error && <div className="bg-red-100 text-red-800 p-3 rounded-lg mb-4">{error}</div>}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div><label className="text-sm font-medium text-on-surface-variant">Nome</label><input type="text" required className="w-full bg-surface-container-low rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-primary" value={form.nome} onChange={e => setForm({ ...form, nome: e.target.value })} /></div>
          <div><label className="text-sm font-medium text-on-surface-variant">E-mail</label><input type="email" required className="w-full bg-surface-container-low rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-primary" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} /></div>
          <div><label className="text-sm font-medium text-on-surface-variant">Senha (mínimo 8 caracteres)</label><input type="password" required minLength="8" className="w-full bg-surface-container-low rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-primary" value={form.senha} onChange={e => setForm({ ...form, senha: e.target.value })} /></div>
          <button type="submit" disabled={loading} className="bg-secondary-container hover:bg-secondary-fixed text-on-secondary-container font-medium py-3 px-6 rounded-lg transition-colors disabled:opacity-50">{loading ? 'Cadastrando...' : 'Cadastrar'}</button>
        </form>
        <p className="text-center mt-4 text-on-surface-variant">Já tem conta? <Link to="/login" className="text-primary hover:underline">Faça login</Link></p>
      </div>
    </div>
  );
};

// ---------- App principal ----------
function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="bg-background font-body-md text-on-background min-h-screen flex flex-col">
          <Header />
          <main className="w-full pt-20 bg-background flex-1">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/catalogo" element={<Catalogo />} />
              <Route path="/veiculo/:id" element={<DetalhesVeiculo />} />
              <Route path="/minhas-reservas" element={<MinhasReservas />} />
              <Route path="/login" element={<Login />} />
              <Route path="/cadastro" element={<Cadastro />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;