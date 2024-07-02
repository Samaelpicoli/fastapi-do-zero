import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_do_zero.app import app
from fastapi_do_zero.database import get_session
from fastapi_do_zero.models import User, table_registry


@pytest.fixture()
def client(session):
    """
    Fixture para criar um cliente de teste para a aplicação FastAPI.

    Esta fixture cria um cliente de teste que pode ser usado para
    fazer requisições à aplicação durante os testes. Ela substitui
    a dependência `get_session` pela sessão de banco de dados
    configurada para testes.

    Args:
        session (Session): Sessão de banco de dados configurada
        para testes.

    Yields:
        TestClient: Um cliente de teste configurado para fazer
        requisições à aplicação.
    """

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


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
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    # Inicia uma sessão de banco de dados
    with Session(engine) as session:
        yield session  # Fornece a sessão para os testes

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    """
    Fixture para criar um usuário de teste no banco de dados.

    Esta fixture adiciona um usuário de teste ao banco de dados
    antes de cada teste que o utilizar. O usuário é adicionado
    e a sessão é confirmada e refrescada para garantir que o
    usuário esteja disponível para os testes.

    Args:
        session (Session): Sessão de banco de dados configurada
        para testes.

    Returns:
        User: Um objeto User representando o usuário de teste.
    """
    user = User(username='Teste', email='teste@teste.com', password='teste')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
