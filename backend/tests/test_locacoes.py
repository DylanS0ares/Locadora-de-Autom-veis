def criar_cliente(client):
    response = client.post(
        "/clientes/",
        json={
            "nome": "Dylan Soares",
            "email": "dylan@email.com",
            "telefone": "3299999999"
        }
    )

    return response.json()["id"]


def criar_veiculo(client):
    response = client.post(
        "/veiculos/",
        json={
            "modelo": "Civic",
            "marca": "Honda",
            "ano": 2024,
            "placa": "ABC1234",
            "disponivel": True
        }
    )

    return response.json()["id"]


def test_criar_locacao(client):
    cliente_id = criar_cliente(client)
    veiculo_id = criar_veiculo(client)

    response = client.post(
        "/locacoes/",
        json={
            "cliente_id": cliente_id,
            "veiculo_id": veiculo_id,
            "data_inicio": "2026-10-10T10:00:00",
            "data_fim": "2026-10-15T10:00:00",
            "valor": 500
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["cliente_id"] == cliente_id
    assert data["veiculo_id"] == veiculo_id
    assert data["valor"] == 500


def test_nao_permitir_veiculo_indisponivel(client):
    cliente1 = criar_cliente(client)
    veiculo = criar_veiculo(client)

    primeira = client.post(
        "/locacoes/",
        json={
            "cliente_id": cliente1,
            "veiculo_id": veiculo,
            "data_inicio": "2026-10-10T10:00:00",
            "data_fim": "2026-10-15T10:00:00",
            "valor": 500
        }
    )

    assert primeira.status_code == 200

    cliente2_response = client.post(
        "/clientes/",
        json={
            "nome": "Joao Silva",
            "email": "joao@email.com",
            "telefone": "3298888888"
        }
    )

    cliente2 = cliente2_response.json()["id"]

    segunda = client.post(
        "/locacoes/",
        json={
            "cliente_id": cliente2,
            "veiculo_id": veiculo,
            "data_inicio": "2026-10-20T10:00:00",
            "data_fim": "2026-10-25T10:00:00",
            "valor": 500
        }
    )

    assert segunda.status_code == 409


def test_data_invalida(client):
    cliente_id = criar_cliente(client)
    veiculo_id = criar_veiculo(client)

    response = client.post(
        "/locacoes/",
        json={
            "cliente_id": cliente_id,
            "veiculo_id": veiculo_id,
            "data_inicio": "2025-01-01T10:00:00",
            "data_fim": "2025-01-02T10:00:00",
            "valor": 500
        }
    )

    assert response.status_code == 422