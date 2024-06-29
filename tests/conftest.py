import pytest
from fastapi.testclient import TestClient

from fastapi_do_zero.app import app


@pytest.fixture()
def client():
    """
    Fixture para criar um cliente de teste para a aplicação FastAPI.

    Esta fixture inicializa um TestClient para a aplicação FastAPI,
    permitindo que os testes façam requisições à aplicação sem precisar
    inicializá-la manualmente.

    Returns:
        TestClient: Um cliente de teste para fazer requisições à aplicação.
    """
    return TestClient(app)
