"""Fixtures compartidas del laboratorio de APIs (Sesión 4).

La configuración vive AQUÍ, una sola vez (DRY):
- base_url: el dominio del SUT.
- auth_headers: patrón de autenticación por header.
- api: el cliente listo para usar, compartido por toda la sesión de pytest.
"""

import json
from pathlib import Path

import pytest
import yaml

from client.api_client import ApiClient

BASE_URL = "https://jsonplaceholder.typicode.com"
DATA_DIR = Path(__file__).parent / "data"


def load_json(nombre: str):
    """Carga un archivo JSON de la carpeta data/."""
    return json.loads((DATA_DIR / nombre).read_text(encoding="utf-8"))


def load_yaml(nombre: str):
    """Carga un archivo YAML de la carpeta data/."""
    return yaml.safe_load((DATA_DIR / nombre).read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def auth_headers() -> dict:
    # JSONPlaceholder no exige token, pero el patrón es idéntico
    # al de una API real: el header viaja en TODOS los requests.
    return {"Authorization": "Bearer token-de-practica-curso-qa"}


@pytest.fixture(scope="session")
def api(base_url: str, auth_headers: dict):
    """Cliente único para toda la corrida: se crea una vez, se cierra al final."""
    client = ApiClient(base_url, headers=auth_headers)
    yield client
    client.close()
