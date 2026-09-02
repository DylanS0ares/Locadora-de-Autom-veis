# 🚗 API Locadora de Automóveis

API REST desenvolvida em **Python** utilizando **FastAPI, SQLAlchemy, Pydantic e PostgreSQL** para gerenciamento de veículos, clientes e locações.

O projeto foi desenvolvido com foco na prática de **Backend, APIs REST, ORM, bancos de dados relacionais, validação de dados, autenticação, autorização, testes automatizados, CRUD, organização de código e implementação de regras de negócio**.

---

## 🎯 Objetivo

Construir uma API para gerenciamento de uma locadora de automóveis, permitindo:

* 🚗 Cadastro e gerenciamento de veículos
* 👤 Cadastro e gerenciamento de clientes
* 🔐 Cadastro e autenticação de usuários
* 📋 Criação e gerenciamento de locações
* 🔄 Controle da disponibilidade dos veículos
* ↩️ Devolução de veículos
* 🔗 Consulta das locações de um cliente
* 🛡️ Controle de acesso baseado no tipo de usuário

A aplicação utiliza relacionamentos entre as entidades e regras de negócio para manter a consistência das locações e da disponibilidade dos veículos.

---

## 🛠️ Tecnologias utilizadas

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **PostgreSQL**
* **SQLite** — utilizado nos testes automatizados
* **psycopg2**
* **Uvicorn**
* **Pytest**
* **HTTPX**
* **Passlib**
* **bcrypt**
* **python-jose**
* **JWT**
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
├── .gitignore
├── requirements.txt
└── README.md
```

A aplicação utiliza uma separação de responsabilidades entre **routers**, **CRUDs**, **schemas**, **models** e componentes de **autenticação e segurança**.

### Responsabilidade dos arquivos

| Arquivo               | Responsabilidade                                        |
| --------------------- | ------------------------------------------------------- |
| `main.py`             | Inicialização da aplicação e registro dos routers       |
| `database.py`         | Configuração do banco e gerenciamento das sessões       |
| `models.py`           | Modelos ORM e estrutura das tabelas                     |
| `schemas.py`          | Schemas Pydantic e validação dos dados                  |
| `security.py`         | Criação e validação dos tokens JWT e controle de acesso |
| `password.py`         | Hash e verificação de senhas                            |
| `crud/veiculos.py`    | Operações de banco relacionadas aos veículos            |
| `crud/clientes.py`    | Operações de banco relacionadas aos clientes            |
| `crud/locacoes.py`    | Operações de banco e regras relacionadas às locações    |
| `crud/usuarios.py`    | Operações relacionadas aos usuários                     |
| `routers/veiculos.py` | Endpoints HTTP relacionados aos veículos                |
| `routers/clientes.py` | Endpoints HTTP relacionados aos clientes                |
| `routers/locacoes.py` | Endpoints HTTP relacionados às locações                 |
| `routers/usuarios.py` | Cadastro e autenticação de usuários                     |
| `tests/`              | Testes automatizados da aplicação                       |

---

# 🏗️ Arquitetura

A aplicação segue uma separação simples entre as responsabilidades:

```text
                         main.py
                            │
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
          Routers        Routers        Routers
              │             │             │
              ↓             ↓             ↓
            CRUD           CRUD           CRUD
              │             │             │
              └─────────────┼─────────────┘
                            ↓
                       SQLAlchemy
                            ↓
                       PostgreSQL
```

Os componentes de autenticação atuam como uma camada adicional:

```text
Requisição HTTP
      ↓
Authentication
      ↓
JWT
      ↓
Autorização
      ↓
Router
      ↓
CRUD
      ↓
SQLAlchemy
      ↓
PostgreSQL
```

### Routers

Os routers são responsáveis por:

* Receber requisições HTTP
* Receber dados através dos schemas
* Utilizar as dependências do FastAPI
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

# 🗄️ Banco de dados

A aplicação utiliza **PostgreSQL** como banco de dados principal e **SQLAlchemy** como ORM.

A conexão utiliza o driver `psycopg2`.

O banco contém as principais tabelas:

```text
usuarios
clientes
veiculos
locacoes
```

O SQLAlchemy realiza o mapeamento entre as classes Python e as tabelas do banco de dados.

Para os testes automatizados, é utilizado um **banco SQLite temporário**, isolado do banco PostgreSQL utilizado pela aplicação.

---

# 🧩 Entidades

O sistema possui quatro entidades principais:

```text
Usuario

Cliente ──────┐
              │
              ↓
           Locacao
              ↑
              │
Veiculo ──────┘
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

### 🔐 Usuário

Representa os usuários que possuem acesso à API.

Campos:

* `id`
* `nome`
* `email`
* `senha_hash`
* `tipo`

O campo `tipo` define o nível de acesso do usuário:

```text
cliente
admin
```

---

# 🔗 Relacionamentos

Os relacionamentos foram implementados utilizando `ForeignKey` e `relationship` do SQLAlchemy.

Uma locação pertence a:

* 1 cliente
* 1 veículo

Enquanto um cliente e um veículo podem estar relacionados a várias locações ao longo do tempo.

---

# 🧩 SQLAlchemy ORM

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

# 📦 Pydantic Schemas

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

### Usuários

```text
UsuarioSchema
UsuarioCreate
LoginSchema
```

Os schemas são utilizados pelo FastAPI para **validação dos dados** e definição do formato das respostas.

Entre as validações implementadas estão:

* Formato e tamanho da placa
* E-mail válido
* Telefone válido
* Ano do veículo
* Valor da locação maior que zero
* Data de início não pode estar no passado
* Data de início deve ser anterior à data de fim
* Senha com tamanho mínimo
* Campos obrigatórios

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

## 🔐 Usuários

| Método | Endpoint          | Função           |
| ------ | ----------------- | ---------------- |
| POST   | `/usuarios/`      | Cadastra usuário |
| POST   | `/usuarios/login` | Realiza login    |

---

# 🔐 Autenticação e autorização

A API utiliza **JWT (JSON Web Token)** para autenticação.

O fluxo de autenticação funciona da seguinte forma:

```text
Cadastro
   ↓
Senha recebe hash
   ↓
Usuário armazenado no PostgreSQL
   ↓
Login
   ↓
Validação de email e senha
   ↓
JWT gerado
   ↓
Token enviado nas requisições protegidas
```

As senhas não são armazenadas diretamente no banco. O projeto utiliza **bcrypt** através do `Passlib` para gerar e verificar os hashes.

### Controle de acesso

A API possui dois tipos de usuário:

```text
cliente
admin
```

O acesso às rotas pode ser controlado através das dependências:

```python
get_usuario_atual
get_admin_atual
```

O `get_usuario_atual` valida o token JWT e identifica o usuário autenticado.

O `get_admin_atual` verifica se o usuário possui permissão de administrador.

Por exemplo, operações administrativas de veículos podem exigir um usuário com:

```text
tipo = admin
```

Caso um usuário autenticado não possua a permissão necessária, a API retorna:

```text
403 Forbidden
```

---

# ⚙️ Regras de negócio

Além das operações CRUD, a API possui regras específicas para o funcionamento da locadora.

## Criação de locação

Antes de criar uma locação, a API verifica:

1. Se o cliente existe.
2. Se o veículo existe.
3. Se o veículo está disponível.
4. Se as datas informadas são válidas.
5. Se o valor da locação é maior que zero.

Após uma locação, o veículo passa automaticamente para indisponível.

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

# 🔒 Validação e tratamento de erros

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
* Dados de entrada inválidos
* Datas de locação inválidas
* Erros de integridade do banco
* Token inválido ou expirado
* Usuário sem permissão

Erros de integridade do banco são tratados através de `IntegrityError`, evitando que exceções do banco sejam expostas diretamente ao cliente da API.

---

# 🧱 Routers e CRUD

A aplicação foi organizada utilizando `APIRouter`, separando os endpoints por entidade.

```text
main.py
   │
   ├── veiculos.router
   ├── clientes.router
   ├── locacoes.router
   └── usuarios.router
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
PostgreSQL
```

Essa separação facilita a manutenção e permite que a lógica de acesso ao banco seja reutilizada por diferentes endpoints.

---

# 💉 Dependency Injection

O projeto utiliza `Depends` do FastAPI para fornecer dependências aos endpoints.

A sessão do banco é fornecida através de:

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Além do gerenciamento das sessões do banco, o sistema utiliza Dependency Injection para autenticação e autorização:

```python
usuario = Depends(get_usuario_atual)
```

e:

```python
usuario = Depends(get_admin_atual)
```

Dessa forma, responsabilidades como acesso ao banco e controle de autenticação ficam centralizadas.

---

# 🧪 Testes automatizados

O projeto utiliza **Pytest** para testar os endpoints e as principais regras de negócio da aplicação.

A estrutura dos testes é:

```text
tests/

├── conftest.py
├── test_veiculos.py
├── test_clientes.py
└── test_locacoes.py
```

O `conftest.py` configura o ambiente de testes e fornece um `TestClient` para realizar requisições à API.

Os testes utilizam um **banco SQLite temporário**, separado do PostgreSQL utilizado pela aplicação.

Dessa forma, os testes não modificam os dados do banco principal.

O ambiente de testes também cria um usuário administrador e gera um token JWT para permitir o teste das rotas protegidas.

### Principais comportamentos testados

* Criação de veículos
* Consulta de veículos
* Atualização de veículos
* Exclusão de veículos
* Criação de clientes
* Atualização de clientes
* Exclusão de clientes
* Criação de locações
* Atualização de locações
* Exclusão de locações
* Validação de veículos indisponíveis
* Devolução de veículos
* Regras de negócio das locações
* Validações de entrada
* E-mails duplicados
* Placas duplicadas
* Tratamento de recursos inexistentes

### Executando os testes

Na raiz do projeto:

```bash
pytest
```

---

# 📖 Documentação da API

A aplicação utiliza **Swagger / OpenAPI** através do FastAPI.

Após iniciar o servidor:

```bash
python -m uvicorn app.main:app --reload
```

A documentação pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

O Swagger permite visualizar os endpoints, schemas, parâmetros e executar requisições diretamente pelo navegador.

As rotas protegidas utilizam autenticação **Bearer Token**.

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

## 3. Configure o PostgreSQL

Crie um banco PostgreSQL para a aplicação e configure a URL de conexão no arquivo:

```text
app/database.py
```

Exemplo:

```python
DATABASE_URL = "postgresql+psycopg2://usuario:senha@127.0.0.1:5432/locadora"
```

> Ajuste usuário, senha, host e porta de acordo com sua instalação do PostgreSQL.

## 4. Execute a aplicação

```bash
python -m uvicorn app.main:app --reload
```

## 5. Acesse a documentação

```text
http://127.0.0.1:8000/docs
```

## 6. Execute os testes

```bash
pytest
```

---

# 📚 Conceitos praticados

Durante o desenvolvimento foram praticados:

* Python
* Programação Orientada a Objetos
* Banco de dados relacional
* PostgreSQL
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
* Pytest
* Testes automatizados
* Fixtures
* `TestClient`
* Banco de dados temporário para testes
* JWT
* Autenticação
* Autorização
* RBAC
* Hash de senhas
* bcrypt
* Tratamento de `IntegrityError`

---

# 🚀 Próximos passos

### Evolução do backend

* [ ] Implementar paginação
* [ ] Adicionar filtros e buscas
* [ ] Melhorar separação das regras de negócio
* [ ] Aumentar a cobertura de testes
* [ ] Melhorar gerenciamento de configurações e variáveis de ambiente
* [ ] Adicionar migrations com Alembic

### Integração

* [ ] Criar frontend para consumir a API
* [ ] Integrar com JavaScript
* [ ] Criar dashboard
* [ ] Realizar deploy da aplicação
* [ ] Containerizar a aplicação com Docker

---

# 📌 Status

**Em desenvolvimento — Projeto de estudo de Backend e APIs REST.**

O projeto atualmente possui:

* ✅ CRUD de veículos
* ✅ CRUD de clientes
* ✅ CRUD de locações
* ✅ CRUD de usuários
* ✅ Camada CRUD para separação da lógica de banco
* ✅ Routers organizados por entidade
* ✅ Relacionamentos entre entidades
* ✅ PostgreSQL
* ✅ SQLAlchemy ORM
* ✅ Validação com Pydantic
* ✅ Validação de datas das locações
* ✅ Tratamento de erros com `HTTPException`
* ✅ Tratamento de erros de integridade do banco
* ✅ Controle de disponibilidade dos veículos
* ✅ Endpoint de devolução
* ✅ Consulta de locações por cliente
* ✅ Consulta de veículos disponíveis
* ✅ Dependency Injection
* ✅ Autenticação com JWT
* ✅ Hash de senhas com bcrypt
* ✅ Autorização baseada em tipo de usuário
* ✅ Controle de acesso para administradores
* ✅ Testes automatizados com Pytest
* ✅ Testes dos endpoints
* ✅ Testes de regras de negócio
* ✅ Banco SQLite temporário para testes
* ✅ Documentação automática com Swagger / OpenAPI

Os próximos passos serão focados na evolução da aplicação, incluindo **paginação, filtros, migrations, Docker, frontend e deploy**.

---

# 👨‍💻 Projeto de estudo

Projeto desenvolvido para consolidar conhecimentos práticos de **Python, desenvolvimento Backend, APIs REST, SQLAlchemy, PostgreSQL, autenticação, autorização, bancos de dados relacionais e testes automatizados**, servindo como etapa de evolução para aplicações mais completas e projetos profissionais.
