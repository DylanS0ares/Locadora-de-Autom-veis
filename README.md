# 🚗 API Locadora de Automóveis

API REST para gerenciamento de uma locadora de veículos, desenvolvida com **Python e FastAPI**, utilizando **PostgreSQL, SQLAlchemy, Pydantic, JWT, Alembic e Docker**.

O projeto foi desenvolvido com foco em práticas de desenvolvimento **Backend**, incluindo arquitetura em camadas, CRUD, ORM, validação de dados, autenticação e autorização, regras de negócio, testes automatizados, migrations e deploy.

## 🌐 Demonstração

**API online:**
`AINDA NAO ARRUMEI O FRONTEND`

Aqui temos uma ideia de como está funcionando a FastAPI e toda a estruturação
**Swagger / OpenAPI:**
`https://locadora-de-autom-veis.onrender.com/docs`

A documentação interativa permite consultar os endpoints, visualizar os schemas e realizar requisições diretamente pelo navegador.

---

## 🎯 Funcionalidades

* 🚗 CRUD de veículos
* 👤 CRUD de clientes
* 🔐 Cadastro e autenticação de usuários
* 🔑 Autenticação utilizando JWT
* 🛡️ Autorização baseada em perfil (`cliente` / `admin`)
* 📋 Criação e gerenciamento de locações
* 🔄 Controle automático da disponibilidade dos veículos
* ↩️ Devolução de veículos
* 🔗 Consulta das locações de um cliente
* ✅ Validação de dados com Pydantic
* 📅 Validação das datas das locações
* 🗄️ Tratamento de erros de integridade do banco
* 🧪 Testes automatizados
* 🔄 Migrations com Alembic
* 🐳 Containerização com Docker
* ☁️ Deploy da aplicação

---

## 🛠️ Tecnologias

| Tecnologia            | Utilização                  |
| --------------------- | --------------------------- |
| **Python**            | Linguagem principal         |
| **FastAPI**           | Desenvolvimento da API REST |
| **SQLAlchemy**        | ORM e acesso ao banco       |
| **PostgreSQL**        | Banco de dados da aplicação |
| **Pydantic**          | Validação e serialização    |
| **Alembic**           | Controle de migrations      |
| **JWT**               | Autenticação                |
| **Passlib + bcrypt**  | Hash de senhas              |
| **Pytest**            | Testes automatizados        |
| **HTTPX**             | Cliente HTTP para testes    |
| **Docker**            | Containerização             |
| **Uvicorn**           | Servidor ASGI               |
| **Swagger / OpenAPI** | Documentação da API         |

---

# 🏗️ Arquitetura

A aplicação utiliza uma separação de responsabilidades entre **routers, CRUDs, schemas, models e autenticação**.

```text
                    Cliente
                       │
                       ▼
                  HTTP Request
                       │
                       ▼
                    Router
                       │
             ┌─────────┴─────────┐
             │                   │
        Autenticação         Validação
             │                   │
             └─────────┬─────────┘
                       ▼
                      CRUD
                       │
                       ▼
                  SQLAlchemy
                       │
                       ▼
                   PostgreSQL
```

A estrutura em camadas evita concentrar toda a lógica nos endpoints e facilita a manutenção e evolução do projeto.

---

# 📁 Estrutura do projeto

```text
locadora-de-automoveis/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── password.py
│   │
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── veiculos.py
│   │   ├── clientes.py
│   │   ├── locacoes.py
│   │   └── usuarios.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── veiculos.py
│       ├── clientes.py
│       ├── locacoes.py
│       └── usuarios.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_veiculos.py
│   ├── test_clientes.py
│   └── test_locacoes.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

### Responsabilidade dos principais componentes

| Componente    | Responsabilidade                                  |
| ------------- | ------------------------------------------------- |
| `main.py`     | Inicialização da aplicação e registro dos routers |
| `database.py` | Configuração do banco e sessões                   |
| `models.py`   | Modelos ORM e estrutura das tabelas               |
| `schemas.py`  | Schemas Pydantic e validação                      |
| `security.py` | JWT e controle de acesso                          |
| `password.py` | Hash e verificação de senhas                      |
| `crud/`       | Operações de banco e regras de negócio            |
| `routers/`    | Endpoints HTTP                                    |
| `tests/`      | Testes automatizados                              |
| `alembic/`    | Controle de migrations                            |

---

# 🗄️ Banco de dados

O projeto utiliza **PostgreSQL** como banco principal e **SQLAlchemy** como ORM.

Principais entidades:

```text
Usuario
   │
   │
Cliente ────────┐
                │
                ▼
             Locacao
                ▲
                │
Veiculo ────────┘
```

### Entidades

#### 🚗 Veículo

Representa os veículos disponíveis para locação.

Principais campos:

```text
id
modelo
marca
ano
placa
quilometragem
disponivel
```

#### 👤 Cliente

```text
id
nome
email
telefone
```

#### 📋 Locação

```text
id
cliente_id
veiculo_id
data_inicio
data_fim
valor
```

`cliente_id` e `veiculo_id` são **Foreign Keys** que relacionam a locação ao cliente e ao veículo.

#### 🔐 Usuário

```text
id
nome
email
senha_hash
tipo
```

Os usuários possuem dois níveis de acesso:

```text
cliente
admin
```

---

# 🧩 SQLAlchemy ORM

O projeto utiliza o padrão **Object-Relational Mapping (ORM)** para representar as entidades do banco através de classes Python.

São utilizados recursos do SQLAlchemy 2:

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

Exemplo:

```python
class Veiculo(Base):
    __tablename__ = "veiculos"

    modelo: Mapped[str] = mapped_column(String(100))
```

---

# 📦 Pydantic

Os schemas Pydantic controlam os dados recebidos e retornados pela API.

Exemplos:

```text
VeiculoCreate
VeiculoUpdate
VeiculoSchema

ClienteCreate
ClienteUpdate
ClienteSchema

LocacaoCreate
LocacaoUpdate
LocacaoSchema

UsuarioCreate
UsuarioSchema
LoginSchema
```

Entre as validações implementadas:

* E-mail válido
* Telefone válido
* Formato da placa
* Ano do veículo
* Valor da locação maior que zero
* Datas de locação válidas
* Data de início anterior à data de fim
* Senha com tamanho mínimo
* Campos obrigatórios

---

# 🌐 Endpoints

## 🚗 Veículos

| Método | Endpoint                 | Descrição                  |
| ------ | ------------------------ | -------------------------- |
| GET    | `/veiculos/`             | Lista veículos             |
| GET    | `/veiculos/{veiculo_id}` | Busca veículo              |
| GET    | `/veiculos/disponiveis`  | Lista veículos disponíveis |
| POST   | `/veiculos/`             | Cria veículo               |
| PUT    | `/veiculos/{veiculo_id}` | Atualiza veículo           |
| DELETE | `/veiculos/{veiculo_id}` | Remove veículo             |

## 👤 Clientes

| Método | Endpoint                          | Descrição                 |
| ------ | --------------------------------- | ------------------------- |
| GET    | `/clientes/`                      | Lista clientes            |
| POST   | `/clientes/`                      | Cria cliente              |
| PUT    | `/clientes/{cliente_id}`          | Atualiza cliente          |
| DELETE | `/clientes/{cliente_id}`          | Remove cliente            |
| GET    | `/clientes/{cliente_id}/locacoes` | Lista locações do cliente |

## 📋 Locações

| Método | Endpoint                          | Descrição        |
| ------ | --------------------------------- | ---------------- |
| GET    | `/locacoes/`                      | Lista locações   |
| POST   | `/locacoes/`                      | Cria locação     |
| PUT    | `/locacoes/{locacao_id}`          | Atualiza locação |
| DELETE | `/locacoes/{locacao_id}`          | Remove locação   |
| POST   | `/locacoes/{locacao_id}/devolver` | Devolve veículo  |

## 🔐 Usuários

| Método | Endpoint          | Descrição        |
| ------ | ----------------- | ---------------- |
| POST   | `/usuarios/`      | Cadastra usuário |
| POST   | `/usuarios/login` | Realiza login    |

---

# 🔐 Autenticação e autorização

A API utiliza **JWT (JSON Web Token)** para autenticação.

Fluxo:

```text
Cadastro
   ↓
Hash da senha
   ↓
Usuário armazenado no PostgreSQL
   ↓
Login
   ↓
Validação de credenciais
   ↓
JWT gerado
   ↓
Bearer Token
   ↓
Endpoint protegido
```

As senhas são armazenadas utilizando **hash bcrypt**, e não em texto puro.

### Controle de acesso

A aplicação utiliza Dependency Injection para controlar as permissões:

```python
get_usuario_atual
get_admin_atual
```

O `get_usuario_atual` valida o JWT e identifica o usuário autenticado.

O `get_admin_atual` verifica se o usuário possui privilégios administrativos.

Quando um usuário autenticado não possui permissão suficiente:

```text
403 Forbidden
```

---

# ⚙️ Regras de negócio

O projeto possui regras para manter a consistência das locações.

### Criação de locação

Antes de criar uma locação:

1. O cliente deve existir.
2. O veículo deve existir.
3. O veículo deve estar disponível.
4. As datas devem ser válidas.
5. O valor deve ser maior que zero.

Após a criação:

```text
Veículo disponível
        ↓
Locação criada
        ↓
Veículo indisponível
```

### Troca de veículo

Quando uma locação é atualizada e o veículo é alterado:

```text
Veículo antigo
      ↓
Disponível

Veículo novo
      ↓
Indisponível
```

### Devolução

Endpoint:

```text
POST /locacoes/{locacao_id}/devolver
```

Após a devolução:

```text
Locação devolvida
       ↓
Veículo liberado
       ↓
disponivel = True
```

---

# 🔒 Tratamento de erros

A API utiliza respostas HTTP adequadas para diferentes situações.

Exemplo:

```python
raise HTTPException(
    status_code=404,
    detail="Veículo não encontrado"
)
```

São tratados casos como:

* Recursos inexistentes
* Veículos indisponíveis
* E-mails duplicados
* Placas duplicadas
* Dados inválidos
* Datas inválidas
* Erros de integridade do banco
* Token inválido ou expirado
* Usuário sem permissão

Erros de integridade utilizam `IntegrityError` para evitar que detalhes internos do banco sejam expostos diretamente ao cliente.

---

# 🧪 Testes automatizados

Os testes são realizados utilizando **Pytest** e **HTTPX**.

```text
tests/
├── conftest.py
├── test_veiculos.py
├── test_clientes.py
└── test_locacoes.py
```

O ambiente de testes utiliza um banco **SQLite separado**, evitando alterações no PostgreSQL utilizado pela aplicação.

São testados comportamentos como:

* CRUD de veículos
* CRUD de clientes
* CRUD de locações
* Criação de locações
* Veículos indisponíveis
* Devolução de veículos
* Atualização de locações
* Exclusão de locações
* Validações de entrada
* Recursos inexistentes
* E-mails duplicados
* Placas duplicadas
* Regras de negócio
* Rotas protegidas

### Executar testes

```bash
pytest
```

---

# 🔄 Migrations

O controle da estrutura do banco é realizado utilizando **Alembic**.

As alterações nos modelos podem ser transformadas em migrations:

```bash
alembic revision --autogenerate -m "descricao da alteracao"
```

E aplicadas ao banco com:

```bash
alembic upgrade head
```

No ambiente Docker/produção, as migrations são executadas antes da inicialização da aplicação.

---

# 🐳 Docker

A aplicação pode ser executada em containers utilizando Docker.

O ambiente possui:

```text
API
 │
 │
 └── PostgreSQL
```

Para iniciar o ambiente:

```bash
docker compose up --build
```

A API ficará disponível localmente em:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Para parar os containers:

```bash
docker compose down
```

---

# ▶️ Execução local

## 1. Clone o projeto

```bash
git clone https://github.com/DylanS0ares/Locadora-de-Autom-veis.git

cd Locadora-de-Autom-veis
```

## 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 3. Configure as variáveis de ambiente

Crie um arquivo `.env`:

```env
DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/locadora
SECRET_KEY=sua_chave_secreta
```

> Não versione o arquivo `.env`. As credenciais devem permanecer fora do repositório.

## 4. Execute as migrations

```bash
alembic upgrade head
```

## 5. Execute a aplicação

```bash
python -m uvicorn app.main:app --reload
```

## 6. Acesse o Swagger

```text
http://127.0.0.1:8000/docs
```

---

# ☁️ Deploy

A aplicação foi containerizada com **Docker** e publicada utilizando **Render**.

A arquitetura de produção utiliza:

```text
Internet
   ↓
Render
   ↓
Docker Container
   ↓
FastAPI
   ↓
PostgreSQL
```

As variáveis sensíveis, como `DATABASE_URL` e `SECRET_KEY`, são configuradas através das variáveis de ambiente do ambiente de produção.

---

# 📚 Principais conceitos praticados

* Python
* FastAPI
* REST API
* HTTP
* JSON
* SQL
* PostgreSQL
* SQLAlchemy
* ORM
* Foreign Keys
* Relationships
* CRUD
* Pydantic
* Dependency Injection
* JWT
* RBAC
* Hash de senhas
* bcrypt
* Tratamento de exceções
* Regras de negócio
* Pytest
* HTTPX
* Fixtures
* Alembic
* Docker
* Docker Compose
* Deploy

---

# 🚀 Próximos passos

Algumas evoluções planejadas para o projeto:

* [ ] Implementar paginação
* [ ] Adicionar filtros e buscas
* [ ] Melhorar cobertura de testes
* [ ] Criar frontend para consumir a API
* [ ] Criar dashboard
* [ ] Adicionar funcionalidades de gerenciamento de frota
* [ ] Melhorar observabilidade e logging

---

# 📌 Status

### 🟢 Projeto funcional e publicado

O backend atualmente possui:

* ✅ CRUD de veículos
* ✅ CRUD de clientes
* ✅ CRUD de locações
* ✅ CRUD de usuários
* ✅ PostgreSQL
* ✅ SQLAlchemy ORM
* ✅ Pydantic
* ✅ JWT
* ✅ Autenticação
* ✅ Autorização
* ✅ RBAC
* ✅ Hash de senhas
* ✅ Regras de negócio
* ✅ Validação de dados
* ✅ Tratamento de erros
* ✅ Testes automatizados
* ✅ Alembic
* ✅ Docker
* ✅ Docker Compose
* ✅ Swagger / OpenAPI
* ✅ Deploy

---

## 👨‍💻 Sobre o projeto

Projeto desenvolvido para consolidar conhecimentos práticos em **desenvolvimento Backend e APIs REST**, explorando desde a modelagem de banco de dados e implementação das regras de negócio até autenticação, testes, migrations, containerização e deploy.

O projeto representa uma aplicação prática de conceitos utilizados no desenvolvimento de APIs modernas com Python.
