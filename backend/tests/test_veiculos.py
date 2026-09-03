def test_criar_veiculo(client):
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

    assert response.status_code == 200

    data = response.json()

    assert data["modelo"] == "Civic"
    assert data["marca"] == "Honda"
    assert data["ano"] == 2024
    assert data["placa"] == "ABC1234"
    assert data["disponivel"] is True


def test_listar_veiculos(client):
    client.post(
        "/veiculos/",
        json={
            "modelo": "Civic",
            "marca": "Honda",
            "ano": 2024,
            "placa": "ABC1234",
            "disponivel": True
        }
    )

    response = client.get("/veiculos/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["modelo"] == "Civic"


def test_buscar_veiculo(client):
    criar = client.post(
        "/veiculos/",
        json={
            "modelo": "Civic",
            "marca": "Honda",
            "ano": 2024,
            "placa": "ABC1234",
            "disponivel": True
        }
    )

    veiculo_id = criar.json()["id"]

    response = client.get(
        f"/veiculos/{veiculo_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == veiculo_id
    assert data["modelo"] == "Civic"


def test_veiculo_nao_encontrado(client):
    response = client.get("/veiculos/999")

    assert response.status_code == 404


def test_listar_veiculos_disponiveis(client):
    client.post(
        "/veiculos/",
        json={
            "modelo": "Civic",
            "marca": "Honda",
            "ano": 2024,
            "placa": "ABC1234",
            "disponivel": True
        }
    )

    client.post(
        "/veiculos/",
        json={
            "modelo": "Corolla",
            "marca": "Toyota",
            "ano": 2023,
            "placa": "XYZ5678",
            "disponivel": False
        }
    )

    response = client.get("/veiculos/disponiveis")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["placa"] == "ABC1234"


def test_placa_duplicada(client):
    veiculo = {
        "modelo": "Civic",
        "marca": "Honda",
        "ano": 2024,
        "placa": "ABC1234",
        "disponivel": True
    }

    primeira = client.post(
        "/veiculos/",
        json=veiculo
    )

    segunda = client.post(
        "/veiculos/",
        json=veiculo
    )

    assert primeira.status_code == 200
    assert segunda.status_code == 409


def test_atualizar_veiculo(client):
    criar = client.post(
        "/veiculos/",
        json={
            "modelo": "Civic",
            "marca": "Honda",
            "ano": 2024,
            "placa": "ABC1234",
            "disponivel": True
        }
    )

    veiculo_id = criar.json()["id"]

    response = client.put(
        f"/veiculos/{veiculo_id}",
        json={
            "modelo": "Corolla",
            "marca": "Toyota",
            "ano": 2025,
            "placa": "XYZ5678",
            "disponivel": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["modelo"] == "Corolla"
    assert data["marca"] == "Toyota"
    assert data["ano"] == 2025
    assert data["placa"] == "XYZ5678"


def test_atualizar_veiculo_inexistente(client):
    response = client.put(
        "/veiculos/999",
        json={
            "modelo": "Corolla",
            "marca": "Toyota",
            "ano": 2025,
            "placa": "XYZ5678",
            "disponivel": True
        }
    )

    assert response.status_code == 404


def test_deletar_veiculo(client):
    criar = client.post(
        "/veiculos/",
        json={
            "modelo": "Civic",
            "marca": "Honda",
            "ano": 2024,
            "placa": "ABC1234",
            "disponivel": True
        }
    )

    veiculo_id = criar.json()["id"]

    response = client.delete(
        f"/veiculos/{veiculo_id}"
    )

    assert response.status_code == 200

    buscar = client.get(
        f"/veiculos/{veiculo_id}"
    )

    assert buscar.status_code == 404


def test_deletar_veiculo_inexistente(client):
    response = client.delete("/veiculos/999")

    assert response.status_code == 404