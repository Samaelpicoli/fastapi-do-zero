import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_do_zero.app import app
from fastapi_do_zero.models import table_registry


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


@pytest.fixture()
def session():
    """
    Fixture para configurar uma sessão de banco de dados em
    memória para testes.

    Esta fixture cria um banco de dados SQLite em memória, configura
    as tabelas usando SQLAlchemy e fornece uma sessão de banco de dados
    para os testes. Após os testes, as tabelas são removidas.

    Yields:
        Session: Uma sessão de banco de dados configurada
        para uso nos testes.
    """
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    # Inicia uma sessão de banco de dados
    with Session(engine) as session:
        yield session  # Fornece a sessão para os testes

    table_registry.metadata.drop_all(engine)
