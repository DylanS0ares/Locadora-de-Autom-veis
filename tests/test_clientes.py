def test_criar_cliente(client):
    response = client.post(
        "/clientes/",
        json={
            "nome": "Dylan Soares",
            "email": "dylan@email.com",
            "telefone": "3299999999"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["nome"] == "Dylan Soares"
    assert data["email"] == "dylan@email.com"


def test_cliente_nao_encontrado(client):
    response = client.put(
        "/clientes/999",
        json={
            "nome": "Dylan Soares",
            "email": "dylan@email.com",
            "telefone": "3299999999"
        }
    )

    assert response.status_code == 404


def test_email_duplicado(client):
    cliente = {
        "nome": "Dylan Soares",
        "email": "dylan@email.com",
        "telefone": "3299999999"
    }

    primeira = client.post(
        "/clientes/",
        json=cliente
    )

    segunda = client.post(
        "/clientes/",
        json=cliente
    )

    assert primeira.status_code == 200
    assert segunda.status_code == 409