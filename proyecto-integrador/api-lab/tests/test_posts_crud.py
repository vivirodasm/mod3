"""Bloque B — CRUD completo con el cliente y las fixtures (DRY).

Es el "reto de la Sesión 3 refactorizado": los mismos 6 requests de la
colección Postman, ahora en Python puro. La fixture `api` ya trae la
base_url y los headers configurados — los tests solo piden y validan.
"""

import time

# Contrato del recurso post: campo -> tipo esperado
CONTRATO_POST = {"userId": int, "id": int, "title": str, "body": str}


def cumple_contrato(recurso: dict, contrato: dict) -> bool:
    """Valida presencia y tipo de cada campo (el JSON Schema de la S3, versión KISS)."""
    return all(
        campo in recurso and isinstance(recurso[campo], tipo)
        for campo, tipo in contrato.items()
    )


def test_listar_posts_devuelve_100(api):
    respuesta = api.get("/posts")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 100


def test_detalle_cumple_el_contrato(api):
    respuesta = api.get("/posts/1")

    assert respuesta.status_code == 200
    assert cumple_contrato(respuesta.json(), CONTRATO_POST)


def test_crear_post_devuelve_201_y_eco_del_payload(api):
    # Título único por corrida — igual que el pre-request script de Postman
    titulo = f"Post QA {time.time_ns()}"
    payload = {"title": titulo, "body": "Creado desde la Sesión 4", "userId": 1}

    respuesta = api.post("/posts", json=payload)

    assert respuesta.status_code == 201
    creado = respuesta.json()
    assert isinstance(creado["id"], int)
    assert creado["title"] == titulo


def test_actualizar_post_con_put(api):
    payload = {"id": 1, "title": "Título actualizado en Sesión 4", "body": "Contenido actualizado", "userId": 1}

    respuesta = api.put("/posts/1", json=payload)

    assert respuesta.status_code == 200
    assert respuesta.json()["title"] == payload["title"]


def test_eliminar_post_devuelve_200_y_body_vacio(api):
    respuesta = api.delete("/posts/1")

    assert respuesta.status_code == 200
    assert respuesta.json() == {}


def test_post_inexistente_devuelve_404(api):
    respuesta = api.get("/posts/999999")

    assert respuesta.status_code == 404
