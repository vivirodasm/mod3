import time


CONTRATO_USER = {
    "id": int,
    "name": str,
    "username": str,
    "email": str,
}


def cumple_contrato(recurso: dict, contrato: dict) -> bool:
    return all(
        campo in recurso and isinstance(recurso[campo], tipo)
        for campo, tipo in contrato.items()
    )


def test_listar_users(api):
    respuesta = api.get("/users")

    assert respuesta.status_code == 200
    usuarios = respuesta.json()
    assert isinstance(usuarios, list)
    assert len(usuarios) == 10


def test_detalle_cumple_contrato(api):
    respuesta = api.get("/users/1")

    assert respuesta.status_code == 200
    usuario = respuesta.json()
    assert cumple_contrato(usuario, CONTRATO_USER)
    assert usuario["id"] == 1


def test_crear_user(api):
    nombre = f"Usuario QA {time.time_ns()}"
    payload = {
        "name": nombre,
        "username": "qa_user",
        "email": "qa_user@example.com",
    }

    respuesta = api.post("/users", json=payload)

    assert respuesta.status_code == 201
    usuario_creado = respuesta.json()
    assert usuario_creado["name"] == nombre
    assert "id" in usuario_creado


def test_actualizar_user(api):
    nombre_actualizado = f"Usuario Actualizado {time.time_ns()}"
    payload = {
        "id": 1,
        "name": nombre_actualizado,
        "username": "updated_user",
        "email": "updated_user@example.com",
    }

    respuesta = api.put("/users/1", json=payload)

    assert respuesta.status_code == 200
    usuario_actualizado = respuesta.json()
    assert usuario_actualizado["name"] == nombre_actualizado
    assert usuario_actualizado["username"] == "updated_user"


def test_eliminar_user(api):
    respuesta = api.delete("/users/1")

    assert respuesta.status_code == 200
    assert respuesta.json() == {}
