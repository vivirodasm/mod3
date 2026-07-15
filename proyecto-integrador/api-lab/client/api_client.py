"""Cliente de API mínimo — principio KISS (Keep It Simple, Stupid).

Una sola clase que envuelve httpx.Client:
- La base_url y los headers se configuran UNA vez (DRY).
- Cada método expone solo lo que los tests necesitan.
- Sin herencia, sin metaclases, sin magia.
"""

import httpx


class ApiClient:
    """Envoltorio delgado sobre httpx.Client para probar APIs REST."""

    def __init__(self, base_url: str, headers: dict | None = None, timeout: float = 10.0) -> None:
        self._http = httpx.Client(
            base_url=base_url,
            headers=headers or {},
            timeout=timeout,
        )

    def get(self, path: str, params: dict | None = None) -> httpx.Response:
        return self._http.get(path, params=params)

    def post(self, path: str, json: dict | None = None) -> httpx.Response:
        return self._http.post(path, json=json)

    def put(self, path: str, json: dict | None = None) -> httpx.Response:
        return self._http.put(path, json=json)

    def delete(self, path: str) -> httpx.Response:
        return self._http.delete(path)

    def close(self) -> None:
        self._http.close()
