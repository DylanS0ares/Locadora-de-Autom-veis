# 🚗 API Locadora de Automóveis

API REST desenvolvida em **Python** utilizando **FastAPI**, **SQLAlchemy**, **Pydantic** e **SQLite** para gerenciamento de veículos, clientes e locações de automóveis.

O projeto foi desenvolvido como prática de **Backend, APIs REST, ORM, banco de dados relacionais, validação de dados, organização de código e regras de negócio**.

---

## 🎯 Objetivo

Construir uma API capaz de gerenciar:

* 🚗 Veículos
* 👤 Clientes
* 📋 Locações

A aplicação utiliza relacionamentos entre as entidades e implementa regras de negócio para controlar a disponibilidade dos veículos durante as locações.

---

## 🛠️ Tecnologias utilizadas

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **SQLite**
* **Uvicorn**
* **Swagger / OpenAPI**

---

## 📁 Estrutura do projeto

```text
locadora-de-automoveis/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── veiculos.py
│       ├── clientes.py
│       └── locacoes.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

A aplicação foi organizada utilizando **routers**, separando os endpoints de acordo com cada entidade.

### Responsabilidade dos arquivos

| Arquivo               | Responsabilidade                                  |
| --------------------- | ------------------------------------------------- |
| `main.py`             | Inicialização da aplicação e registro dos routers |
| `database.py`         | Configuração do banco e gerenciamento das sessões |
| `models.py`           | Modelos ORM e estrutura das tabelas               |
| `schemas.py`          | Schemas Pydantic para validação dos dados         |
| `routers/veiculos.py` | Endpoints relacionados aos veículos               |
| `routers/clientes.py` | Endpoints relacionados aos clientes               |
| `routers/locacoes.py` | Endpoints relacionados às locações                |

---

## 🗄️ Banco de dados

O projeto utiliza **SQLite** como banco de dados, com **SQLAlchemy** como ORM.

A conexão utiliza:

```python
DATABASE_URL = "sqlite:///./locadora.db"
```

O SQLAlchemy realiza o mapeamento entre as classes Python e as tabelas do banco de dados.

---

## 🧩 Entidades

O sistema possui três entidades principais:

```text
Cliente
   │
   │ 1:N
   ↓
Locacao
   ↑
   │ N:1
   │
Veiculo
```

### 🚗 Veículo

Representa os automóveis disponíveis para locação.

Campos:

* `id`
* `modelo`
* `marca`
* `ano`
* `placa`
* `disponivel`

### 👤 Cliente

Representa os clientes cadastrados.

Campos:

* `id`
* `nome`
* `email`
* `telefone`

### 📋 Locação

Representa uma locação realizada por um cliente.

Campos:

* `id`
* `cliente_id`
* `veiculo_id`
* `data_inicio`
* `data_fim`
* `valor`

`cliente_id` e `veiculo_id` são **Foreign Keys** utilizadas para relacionar uma locação com um cliente e um veículo.

---

## 🔗 Relacionamentos

Os relacionamentos foram implementados utilizando `ForeignKey` e `relationship` do SQLAlchemy.

Uma locação está relacionada a:

```text
1 Cliente
1 Veículo
```

Enquanto um cliente e um veículo podem possuir várias locações ao longo do tempo.

---

## 🧩 SQLAlchemy ORM

O projeto utiliza o conceito de **ORM (Object-Relational Mapping)**.

As tabelas são representadas por classes Python.

Exemplo:

```python
class Veiculo(Base):
    __tablename__ = "veiculos"
```

Os campos utilizam o sistema moderno de tipagem do SQLAlchemy:

```python
modelo: Mapped[str] = mapped_column(String(100))
```

Também foram utilizados:

* `DeclarativeBase`
* `Mapped`
* `mapped_column`
* `ForeignKey`
* `relationship`
* `Session`
* `select`
* `db.add()`
* `db.add_all()`
* `db.commit()`
* `db.refresh()`
* `db.delete()`
* `db.scalar()`
* `db.scalars()`

---

## 📦 Pydantic Schemas

Foram criados schemas específicos para controlar os dados recebidos e enviados pela API.

### Veículos

```text
VeiculoSchema
VeiculoCreate
VeiculoUpdate
```

### Clientes

```text
ClienteSchema
ClienteCreate
ClienteUpdate
```

### Locações

```text
LocacaoSchema
LocacaoCreate
LocacaoUpdate
```

Os schemas são utilizados pelo FastAPI para **validação dos dados** e definição do formato das respostas.

---

# 🌐 API REST

A API utiliza os principais métodos HTTP:

* `GET` → consulta
* `POST` → criação
* `PUT` → atualização
* `DELETE` → exclusão

## 🚗 Veículos

| Método | Endpoint                 | Função                     |
| ------ | ------------------------ | -------------------------- |
| GET    | `/veiculos/`             | Lista veículos             |
| POST   | `/veiculos/`             | Cria veículo               |
| PUT    | `/veiculos/{veiculo_id}` | Atualiza veículo           |
| DELETE | `/veiculos/{veiculo_id}` | Remove veículo             |
| GET    | `/veiculos/disponiveis`  | Lista veículos disponíveis |

## 👤 Clientes

| Método | Endpoint                          | Função                    |
| ------ | --------------------------------- | ------------------------- |
| GET    | `/clientes/`                      | Lista clientes            |
| POST   | `/clientes/`                      | Cria cliente              |
| PUT    | `/clientes/{cliente_id}`          | Atualiza cliente          |
| DELETE | `/clientes/{cliente_id}`          | Remove cliente            |
| GET    | `/clientes/{cliente_id}/locacoes` | Lista locações do cliente |

## 📋 Locações

| Método | Endpoint                          | Função           |
| ------ | --------------------------------- | ---------------- |
| GET    | `/locacoes/`                      | Lista locações   |
| POST   | `/locacoes/`                      | Cria locação     |
| PUT    | `/locacoes/{locacao_id}`          | Atualiza locação |
| DELETE | `/locacoes/{locacao_id}`          | Remove locação   |
| POST   | `/locacoes/{locacao_id}/devolver` | Devolve veículo  |

---

# ⚙️ Regras de negócio

O projeto possui regras além das operações CRUD básicas.

## Criação de locação

Antes de criar uma locação, a API verifica:

1. Se o cliente existe.
2. Se o veículo existe.
3. Se o veículo está disponível.

Após uma locação:

```text
Veículo disponível
       ↓
Locação criada
       ↓
Veículo indisponível
```

---

## Atualização de locação

Ao alterar o veículo de uma locação, a API verifica se o novo veículo está disponível.

Quando ocorre a troca:

```text
Veículo antigo
       ↓
fica disponível

Veículo novo
       ↓
fica indisponível
```

Isso mantém o estado dos veículos consistente com as locações.

---

## Devolução de veículo

Foi criado um endpoint específico para devolução:

```text
POST /locacoes/{locacao_id}/devolver
```

A API localiza a locação e o veículo relacionado e altera:

```python
veiculo.disponivel = True
```

Assim, o veículo volta a estar disponível para uma nova locação.

---

## Exclusão de locação

Ao excluir uma locação, o veículo relacionado também é liberado:

```text
Locação excluída
       ↓
Veículo liberado
       ↓
disponivel = True
```

---

## 🔒 Validação de dados e erros

A API utiliza `HTTPException` para retornar respostas HTTP apropriadas quando ocorre algum problema.

Exemplo:

```python
raise HTTPException(
    status_code=404,
    detail="Veículo não encontrado"
)
```

Também existem validações para evitar situações como:

* Cliente inexistente
* Veículo inexistente
* Locação inexistente
* Veículo indisponível
* E-mail de cliente duplicado
* Placa de veículo duplicada

---

# 🧱 Organização com Routers

A aplicação foi refatorada utilizando `APIRouter`.

Em vez de concentrar todos os endpoints no `main.py`, cada entidade possui seu próprio router:

```text
main.py
   │
   ├── veiculos.router
   ├── clientes.router
   └── locacoes.router
```

Isso melhora a organização e facilita a manutenção do projeto.

O `main.py` fica responsável principalmente por inicializar a aplicação e registrar os routers.

---

# 💉 Dependency Injection

O projeto utiliza o `Depends` do FastAPI para fornecer uma sessão do banco de dados aos endpoints.

Exemplo:

```python
def lista_veiculos(
    db: Session = Depends(get_db)
):
```

A função `get_db()` cria a sessão e garante seu fechamento após a utilização:

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Dessa forma, a criação e o encerramento das sessões são centralizados.

---

# 🧪 Testes da API

Os endpoints podem ser testados utilizando a documentação automática do FastAPI.

Após iniciar o servidor:

```bash
python -m uvicorn app.main:app --reload
```

A documentação pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

O Swagger permite testar diretamente os endpoints utilizando:

* GET
* POST
* PUT
* DELETE

sem necessidade de um frontend.

---

# ▶️ Como executar

## 1. Instalar as dependências

```bash
pip install fastapi sqlalchemy uvicorn
```

Ou utilizando o arquivo de dependências:

```bash
pip install -r requirements.txt
```

## 2. Executar a aplicação

A partir da pasta raiz:

```bash
python -m uvicorn app.main:app --reload
```

## 3. Acessar a documentação

```text
http://127.0.0.1:8000/docs
```

---

# 📚 Conceitos praticados

Durante o desenvolvimento foram praticados:

* Python
* Programação Orientada a Objetos
* Banco de dados relacional
* SQLite
* SQLAlchemy
* ORM
* Models
* Foreign Keys
* Relationships
* Sessions
* CRUD
* FastAPI
* REST
* HTTP
* JSON
* Pydantic
* Schemas
* Dependency Injection
* `Depends`
* Validação de dados
* `HTTPException`
* Regras de negócio
* Routers
* Organização de projetos Python
* Swagger / OpenAPI

---

# 🚀 Próximos passos

O projeto já possui uma estrutura funcional de backend. Os próximos passos serão focados em melhorar qualidade, arquitetura e recursos.

### Refatoração

* [ ] Criar camada `crud/`
* [ ] Separar lógica de acesso ao banco dos routers
* [ ] Melhorar organização das regras de negócio

### Validação

* [ ] Validar datas das locações
* [ ] Impedir datas inválidas
* [ ] Melhorar validações dos schemas
* [ ] Melhorar tratamento de possíveis erros de banco

### Qualidade

* [ ] Criar testes automatizados
* [ ] Criar testes dos endpoints
* [ ] Testar regras de negócio
* [ ] Melhorar documentação da API

### Evolução do backend

* [ ] Migrar SQLite para PostgreSQL
* [ ] Adicionar autenticação
* [ ] Adicionar usuários e permissões
* [ ] Implementar paginação
* [ ] Adicionar filtros e buscas

### Integração

* [ ] Criar frontend para consumir a API
* [ ] Integrar com JavaScript
* [ ] Criar dashboard
* [ ] Realizar deploy da aplicação

---

# 📌 Status

**Em desenvolvimento — Projeto de estudo de Backend e APIs REST.**

O projeto já possui uma API funcional utilizando **FastAPI + SQLAlchemy + SQLite**, com:

* CRUD de veículos
* CRUD de clientes
* CRUD de locações
* Relacionamentos entre entidades
* Validação com Pydantic
* Tratamento de erros com `HTTPException`
* Controle de disponibilidade dos veículos
* Endpoint de devolução
* Consulta de locações por cliente
* Consulta de veículos disponíveis
* Organização utilizando routers
* Dependency Injection para sessões do banco

O próximo estágio será evoluir a arquitetura com uma camada **CRUD**, adicionar testes automatizados e posteriormente integrar a API com um frontend.

---

## 👨‍💻 Projeto de estudo

Projeto desenvolvido para consolidar conhecimentos práticos de **Python, SQLAlchemy, bancos de dados relacionais, APIs REST e desenvolvimento Backend**, servindo como etapa de evolução para projetos mais completos e aplicações profissionais.
