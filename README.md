# 🚗 API Locadora de Automóveis

API REST desenvolvida em **Python** com **FastAPI**, **SQLAlchemy** e **SQLite** para gerenciamento de veículos, clientes e locações de automóveis.

O projeto foi desenvolvido como prática de **Backend, APIs REST, ORM, banco de dados relacional e integração entre entidades**.

## 🎯 Objetivo

Construir uma API capaz de realizar o gerenciamento de:

* 🚗 Veículos
* 👤 Clientes
* 📋 Locações

O projeto também utiliza relacionamentos entre as entidades para representar o funcionamento básico de uma locadora de veículos.

## 🛠️ Tecnologias utilizadas

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **SQLite**
* **Uvicorn**
* **Swagger / OpenAPI**

## 📁 Estrutura do projeto

```text
locadora-de-automoveis/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── database.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## 🗄️ Banco de dados

O projeto utiliza **SQLite** como banco de dados.

A conexão é configurada através do SQLAlchemy:

```python
DATABASE_URL = "sqlite:///./locadora.db"
```

O SQLAlchemy é responsável pelo mapeamento entre as classes Python e as tabelas do banco.

### Entidades

O banco possui três entidades principais:

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

### Veiculo

Representa os veículos disponíveis na locadora.

Campos:

* `id`
* `modelo`
* `marca`
* `ano`
* `placa`
* `disponivel`

### Cliente

Representa os clientes cadastrados.

Campos:

* `id`
* `nome`
* `email`
* `telefone`

### Locacao

Representa uma locação realizada por um cliente.

Campos:

* `id`
* `cliente_id`
* `veiculo_id`
* `data_inicio`
* `data_fim`
* `valor`

Os campos `cliente_id` e `veiculo_id` são **Foreign Keys** que relacionam a locação com um cliente e um veículo.

## 🔗 Relacionamentos

Foi utilizado o sistema de relacionamentos do SQLAlchemy através de `ForeignKey` e `relationship`.

Uma locação possui:

```text
1 Cliente
1 Veículo
```

Enquanto um cliente ou veículo pode estar relacionado a várias locações ao longo do tempo.

## 🧩 SQLAlchemy ORM

O projeto utiliza o **ORM (Object-Relational Mapping)** do SQLAlchemy.

As tabelas são representadas por classes Python:

```python
class Veiculo(Base):
    __tablename__ = "veiculos"
```

E os campos utilizam `Mapped` e `mapped_column`:

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

## 📦 Pydantic Schemas

Foram criados schemas para controlar os dados recebidos e enviados pela API.

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

Os schemas são utilizados pelo FastAPI para validação e definição do formato dos dados.

## 🌐 API REST

A API foi construída utilizando FastAPI.

### Veículos

| Método | Endpoint                 | Função           |
| ------ | ------------------------ | ---------------- |
| GET    | `/veiculos`              | Lista veículos   |
| POST   | `/veiculos`              | Cria veículo     |
| PUT    | `/veiculos/{veiculo_id}` | Atualiza veículo |
| DELETE | `/veiculos/{veiculo_id}` | Remove veículo   |

### Clientes

| Método | Endpoint                 | Função           |
| ------ | ------------------------ | ---------------- |
| GET    | `/clientes`              | Lista clientes   |
| POST   | `/clientes`              | Cria cliente     |
| PUT    | `/clientes/{cliente_id}` | Atualiza cliente |
| DELETE | `/clientes/{cliente_id}` | Remove cliente   |

### Locações

| Método | Endpoint                 | Função           |
| ------ | ------------------------ | ---------------- |
| GET    | `/locacoes`              | Lista locações   |
| POST   | `/locacoes`              | Cria locação     |
| PUT    | `/locacoes/{locacao_id}` | Atualiza locação |
| DELETE | `/locacoes/{locacao_id}` | Remove locação   |

## ⚙️ Regras de negócio implementadas

O projeto não possui apenas operações CRUD. Algumas regras básicas foram implementadas.

### Criação de locação

Antes de criar uma locação, a API verifica:

1. Se o cliente existe.
2. Se o veículo existe.
3. Se o veículo está disponível.

Após a criação da locação:

```text
Veículo disponível
        ↓
    locação criada
        ↓
Veículo indisponível
```

### Atualização de locação

Ao trocar o veículo de uma locação:

```text
Veículo antigo
      ↓
fica disponível

Veículo novo
      ↓
fica indisponível
```

Isso mantém o estado dos veículos consistente com as locações.

### Exclusão de locação

Ao excluir uma locação, o veículo relacionado volta a ficar disponível.

```text
Locação excluída
       ↓
Veículo liberado
       ↓
disponivel = True
```

## 🧪 Testes da API

Os endpoints podem ser testados através da documentação automática do FastAPI.

Após iniciar o servidor:

```bash
python -m uvicorn app.main:app --reload
```

acesse:

```text
http://127.0.0.1:8000/docs
```

O Swagger permite testar diretamente:

* GET
* POST
* PUT
* DELETE

sem necessidade de um frontend.

## ▶️ Como executar

### 1. Instalar as dependências

```bash
pip install fastapi sqlalchemy uvicorn
```

### 2. Executar a aplicação

A partir da pasta raiz do projeto:

```bash
python -m uvicorn app.main:app --reload
```

### 3. Acessar a documentação

```text
http://127.0.0.1:8000/docs
```

## 📚 Conceitos praticados

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
* Dependency Injection com `Depends`
* Validação de dados
* Regras de negócio
* Swagger / OpenAPI
* Organização de projeto Python

## 🚀 Próximos passos

O projeto ainda pode evoluir para uma aplicação de backend mais completa.

Possíveis melhorias:

* [ ] Melhorar tratamento de erros utilizando `HTTPException`
* [ ] Adicionar validações mais completas
* [ ] Impedir placas e e-mails duplicados
* [ ] Validar datas das locações
* [ ] Criar endpoint específico para devolução de veículos
* [ ] Criar consultas de locações por cliente
* [ ] Criar endpoint para listar veículos disponíveis
* [ ] Melhorar a organização do código em `routers` e `crud`
* [ ] Adicionar testes automatizados
* [ ] Migrar de SQLite para PostgreSQL
* [ ] Adicionar autenticação
* [ ] Criar frontend para consumir a API
* [ ] Realizar deploy da aplicação

## 📌 Status

**Em desenvolvimento — etapa de aprendizado de Backend e APIs.**

O projeto já possui uma API funcional com **FastAPI + SQLAlchemy + SQLite**, CRUD completo para veículos, clientes e locações, além de relacionamentos e regras básicas de negócio.

---

## 👨‍💻 Projeto de estudo

Projeto desenvolvido com o objetivo de consolidar conhecimentos de **Python, bancos de dados, APIs REST e desenvolvimento Backend**, servindo como parte da evolução prática em programação.
