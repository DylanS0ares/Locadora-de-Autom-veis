# 🚗 API Locadora de Automóveis

API REST desenvolvida em **Python** utilizando **FastAPI, SQLAlchemy, Pydantic e SQLite** para gerenciamento de veículos, clientes e locações.

O projeto foi desenvolvido com foco em prática de **Backend, APIs REST, ORM, bancos de dados relacionais, validação de dados, CRUD, organização de código e implementação de regras de negócio**.

---

## 🎯 Objetivo

Construir uma API para gerenciamento de uma locadora de automóveis, permitindo:

* 🚗 Cadastro e gerenciamento de veículos
* 👤 Cadastro e gerenciamento de clientes
* 📋 Criação e gerenciamento de locações
* 🔄 Controle da disponibilidade dos veículos
* ↩️ Devolução de veículos
* 🔗 Consulta das locações de um cliente

A aplicação utiliza relacionamentos entre as entidades e regras de negócio para manter a consistência das locações e da disponibilidade dos veículos.

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
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── veiculos.py
│   │   ├── clientes.py
│   │   └── locacoes.py
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

A aplicação utiliza uma separação de responsabilidades entre **routers** e **CRUDs**.

### Responsabilidade dos arquivos

| Arquivo               | Responsabilidade                                     |
| --------------------- | ---------------------------------------------------- |
| `main.py`             | Inicialização da aplicação e registro dos routers    |
| `database.py`         | Configuração do banco e gerenciamento das sessões    |
| `models.py`           | Modelos ORM e estrutura das tabelas                  |
| `schemas.py`          | Schemas Pydantic para validação dos dados            |
| `crud/veiculos.py`    | Operações de banco relacionadas aos veículos         |
| `crud/clientes.py`    | Operações de banco relacionadas aos clientes         |
| `crud/locacoes.py`    | Operações de banco e regras relacionadas às locações |
| `routers/veiculos.py` | Endpoints HTTP relacionados aos veículos             |
| `routers/clientes.py` | Endpoints HTTP relacionados aos clientes             |
| `routers/locacoes.py` | Endpoints HTTP relacionados às locações              |

---

## 🏗️ Arquitetura

A aplicação segue uma separação simples entre as responsabilidades:

```text
                     main.py
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
      Veículos       Clientes      Locações
       Router         Router        Router
          │             │             │
          ↓             ↓             ↓
        CRUD           CRUD          CRUD
          │             │             │
          └─────────────┼─────────────┘
                        ↓
                   SQLAlchemy
                        ↓
                     SQLite
```

### Routers

Os routers são responsáveis por:

* Receber requisições HTTP
* Receber dados através dos schemas
* Chamar as funções da camada CRUD
* Tratar erros HTTP
* Retornar as respostas da API

### CRUD

A camada `crud/` concentra as operações relacionadas ao banco de dados, como:

* Consultas
* Inserções
* Atualizações
* Exclusões
* Alterações de disponibilidade
* Regras relacionadas às operações das entidades

Dessa forma, a lógica de acesso ao banco não fica concentrada nos routers.

---

## 🗄️ Banco de dados

O projeto utiliza **SQLite** como banco de dados e **SQLAlchemy** como ORM.

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

Representa os veículos disponíveis para locação.

Campos:

* `id`
* `modelo`
* `marca`
* `ano`
* `placa`
* `disponivel`

### 👤 Cliente

Representa os clientes cadastrados no sistema.

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

Uma locação pertence a:

* 1 cliente
* 1 veículo

Enquanto um cliente e um veículo podem estar relacionados a várias locações ao longo do tempo.

---

## 🧩 SQLAlchemy ORM

O projeto utiliza **ORM (Object-Relational Mapping)** para representar as tabelas do banco através de classes Python.

Exemplo:

```python
class Veiculo(Base):

    __tablename__ = "veiculos"
```

Os campos utilizam o sistema moderno de tipagem do SQLAlchemy:

```python
modelo: Mapped[str] = mapped_column(String(100))
```

Também foram utilizados conceitos e recursos como:

* `DeclarativeBase`
* `Mapped`
* `mapped_column`
* `ForeignKey`
* `relationship`
* `Session`
* `select`
* `db.add()`
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

| Método   | Utilização  |
| -------- | ----------- |
| `GET`    | Consulta    |
| `POST`   | Criação     |
| `PUT`    | Atualização |
| `DELETE` | Exclusão    |

## 🚗 Veículos

| Método | Endpoint                 | Função                     |
| ------ | ------------------------ | -------------------------- |
| GET    | `/veiculos/`             | Lista veículos             |
| GET    | `/veiculos/{veiculo_id}` | Busca veículo por ID       |
| GET    | `/veiculos/disponiveis`  | Lista veículos disponíveis |
| POST   | `/veiculos/`             | Cria veículo               |
| PUT    | `/veiculos/{veiculo_id}` | Atualiza veículo           |
| DELETE | `/veiculos/{veiculo_id}` | Remove veículo             |

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

Além das operações CRUD, a API possui regras específicas para o funcionamento da locadora.

## Criação de locação

Antes de criar uma locação, a API verifica:

1. Se o cliente existe.
2. Se o veículo existe.
3. Se o veículo está disponível.

Após uma locação, o veículo passa automaticamente para indisponível:

```text
Veículo disponível
       ↓
Locação criada
       ↓
Veículo indisponível
```

---

## Atualização de locação

Ao alterar uma locação, a API verifica se o cliente e o novo veículo existem.

Caso o veículo seja alterado, o sistema verifica sua disponibilidade.

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

A API localiza a locação e o veículo relacionado e altera sua disponibilidade:

```python
veiculo.disponivel = True
```

O veículo pode então ser utilizado em uma nova locação.

---

## Exclusão de locação

Ao excluir uma locação, o veículo relacionado é liberado:

```text
Locação excluída
       ↓
Veículo liberado
       ↓
disponivel = True
```

---

## 🔒 Validação e tratamento de erros

A API utiliza `HTTPException` para retornar respostas HTTP adequadas quando ocorre algum problema.

Exemplo:

```python
raise HTTPException(
    status_code=404,
    detail="Veículo não encontrado"
)
```

São tratadas situações como:

* Cliente inexistente
* Veículo inexistente
* Locação inexistente
* Veículo indisponível
* E-mail de cliente duplicado
* Placa de veículo duplicada

---

# 🧱 Routers e CRUD

A aplicação foi organizada utilizando `APIRouter`, separando os endpoints por entidade.

```text
main.py
   │
   ├── veiculos.router
   ├── clientes.router
   └── locacoes.router
```

Cada router recebe as requisições relacionadas à sua entidade e delega as operações de banco para sua respectiva camada CRUD.

Exemplo:

```text
POST /veiculos/
       ↓
routers/veiculos.py
       ↓
crud/veiculos.py
       ↓
SQLAlchemy
       ↓
SQLite
```

Essa separação facilita a manutenção e permite que a lógica de acesso ao banco seja reutilizada por diferentes endpoints.

---

# 💉 Dependency Injection

O projeto utiliza `Depends` do FastAPI para fornecer uma sessão do banco de dados aos endpoints.

Exemplo:

```python
def lista_veiculos(
    db: Session = Depends(get_db)
):
```

A função `get_db()` cria a sessão e garante seu encerramento:

```python
def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Dessa forma, o gerenciamento das sessões do banco fica centralizado.

---

# 🧪 Testando a API

Os endpoints podem ser testados através da documentação automática do FastAPI.

Após iniciar o servidor:

```bash
python -m uvicorn app.main:app --reload
```

Acesse:

```text
http://127.0.0.1:8000/docs
```

O Swagger permite executar os endpoints diretamente pelo navegador, sem necessidade de um frontend.

---

# ▶️ Como executar

## 1. Clone o projeto

```bash
git clone https://github.com/DylanS0ares/Locadora-de-Autom-veis.git
cd Locadora-de-Autom-veis
```

## 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 3. Execute a aplicação

```bash
python -m uvicorn app.main:app --reload
```

## 4. Acesse a documentação

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
* [ ] Melhorar separação das regras de negócio

### Integração

* [ ] Criar frontend para consumir a API
* [ ] Integrar com JavaScript
* [ ] Criar dashboard
* [ ] Realizar deploy da aplicação

---

# 📌 Status

**Em desenvolvimento — Projeto de estudo de Backend e APIs REST.**

O projeto atualmente possui:

* ✅ CRUD de veículos
* ✅ CRUD de clientes
* ✅ CRUD de locações
* ✅ Camada CRUD para separação da lógica de banco
* ✅ Routers organizados por entidade
* ✅ Relacionamentos entre entidades
* ✅ Validação com Pydantic
* ✅ Tratamento de erros com `HTTPException`
* ✅ Controle de disponibilidade dos veículos
* ✅ Endpoint de devolução
* ✅ Consulta de locações por cliente
* ✅ Consulta de veículos disponíveis
* ✅ Dependency Injection para sessões do banco
* ✅ Documentação automática com Swagger / OpenAPI

Os próximos passos serão focados em **testes automatizados, melhoria das validações, evolução das regras de negócio e integração com um frontend**.

---

## 👨‍💻 Projeto de estudo

Projeto desenvolvido para consolidar conhecimentos práticos de **Python, desenvolvimento Backend, APIs REST, SQLAlchemy e bancos de dados relacionais**, servindo como etapa de evolução para aplicações mais completas e projetos profissionais.
