import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_do_zero.app import app
from fastapi_do_zero.database import get_session
from fastapi_do_zero.models import User, table_registry
from fastapi_do_zero.security import get_password_hash


class UserFactory(factory.Factory):
    """
    Fábrica para criar instâncias do modelo User para testes.

    A classe UserFactory utiliza a biblioteca factory_boy para gerar
    dados fictícios consistentes e previsíveis para os testes. Os
    atributos username, email e password são gerados automaticamente
    usando as funções de factory_boy.

    Attributes:
        Meta (class): Classe interna que define qual modelo a fábrica
        irá construir.
        username (str): Nome de usuário gerado sequencialmente.
        email (str): Email gerado a partir do username.
        password (str): Senha gerada a partir do username.
    """

    class Meta:
        """
        Define quem a classe irá construir utilizando o parâmetro model.
        """

        model = User

    username = factory.sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}+senha')


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
    pwd = 'teste'
    user = UserFactory(
        password=get_password_hash(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'teste'  # Monkey Patch para guardar a senha og

    return user


@pytest.fixture()
def other_user(session):
    """
    Fixture para criar um segundo usuário de teste no banco de dados.

    Esta fixture adiciona um segundo usuário de teste ao banco de dados
    antes de cada teste que o utilizar. O usuário é criado utilizando
    a UserFactory, adicionado à sessão do banco de dados, confirmado e
    refrescado para garantir que esteja disponível para os testes.

    Args:
        session (Session): Sessão de banco de dados configurada
        para testes.

    Returns:
        User: Um objeto User representando o segundo usuário de teste.
    """
    # Cria um usuário utilizando a UserFactory
    user = UserFactory()

    # Adiciona o usuário à sessão do banco de dados
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture()
def token(client, user):
    """
    Fixture para obter um token de autenticação.

    Esta fixture faz uma requisição para obter um token de
    autenticação usando o usuário de teste criado. O token é
    retornado para uso nos testes.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.
        user (User): O usuário de teste criado.

    Returns:
        str: O token de acesso obtido.
    """
    response = client.post(
        'auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    return response.json()['access_token']
