"""Bloque A — httpx directo, sin cliente ni fixtures.

Estos tests muestran la transición desde Postman: cada uno es el
equivalente Python de lo que hacíamos con Send + pm.test().
Después (Bloque B) veremos por qué repetir la URL en cada test es un problema.
"""

import httpx

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_post_devuelve_200_y_el_recurso():
    respuesta = httpx.get(f"{BASE_URL}/posts/1")

    assert respuesta.status_code == 200
    post = respuesta.json()
    assert post["id"] == 1
    assert post["userId"] == 1


def test_content_type_es_json():
    respuesta = httpx.get(f"{BASE_URL}/posts/1")

    assert "application/json" in respuesta.headers["Content-Type"]


def test_responde_en_menos_de_dos_segundos():
    respuesta = httpx.get(f"{BASE_URL}/posts")

    assert respuesta.elapsed.total_seconds() < 2.0


def test_post_inexistente_devuelve_404():
    respuesta = httpx.get(f"{BASE_URL}/posts/999999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {}
