"""Bloque C — Data-Driven Testing aplicado a APIs.

Los payloads viven en data/ (JSON y YAML), NO en el código.
Agregar un caso nuevo = agregar una entrada al archivo. Cero código nuevo.
"""

import pytest

from conftest import load_json, load_yaml

CASOS_POST = load_json("posts_payloads.json")
CASOS_PUT = load_yaml("update_cases.yaml")["casos"]


@pytest.mark.parametrize(
    "caso",
    CASOS_POST,
    ids=[c["caso"] for c in CASOS_POST],
)
def test_crear_post_con_datos_externos(api, caso):
    respuesta = api.post("/posts", json=caso["payload"])

    assert respuesta.status_code == 201
    creado = respuesta.json()
    # La API hace eco del payload: cada campo enviado debe volver igual
    for campo, valor in caso["payload"].items():
        assert creado[campo] == valor


@pytest.mark.parametrize(
    "caso",
    CASOS_PUT,
    ids=[c["nombre"] for c in CASOS_PUT],
)
def test_actualizar_post_con_datos_externos(api, caso):
    respuesta = api.put(f"/posts/{caso['post_id']}", json=caso["payload"])

    assert respuesta.status_code == 200
    actualizado = respuesta.json()
    assert actualizado["title"] == caso["payload"]["title"]
    assert actualizado["body"] == caso["payload"]["body"]
