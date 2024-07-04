from http import HTTPStatus

from fastapi_do_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    """
    Teste para o endpoint raiz, que deve retornar status
    HTTP 200 e a mensagem 'Olá Mundo!'.

    O teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste.
    2. Act (Ação): Faz uma requisição GET para o endpoint raiz.
    3. Assert (Garantia): Verifica se o status da resposta é 200 OK
    e se a mensagem retornada é 'Olá Mundo!'.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.

    Raises:
        AssertionError: Se o status da resposta não for 200 OK
        ou se a mensagem retornada não for 'Olá Mundo!'.
    """
    response = client.get('/')  # Fase 2: Act (Ação)

    # Fase 3: Assert (Garantia)
    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    """
    Teste para o endpoint de criação de usuário, que deve retornar
    status HTTP 201 e os dados públicos do usuário criado.

    O teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste.
    2. Act (Ação): Faz uma requisição POST para o endpoint de
    criação de usuário com os dados do usuário.
    3. Assert (Garantia): Verifica se o status da resposta é 201
    Created e se os dados retornados correspondem ao esperado.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.

    Raises:
        AssertionError: Se o status da resposta não for 201 Created
        ou se os dados retornados não corresponderem ao esperado.
    """
    response = client.post(
        '/users/',
        json={
            'username': 'Samael',
            'email': 'sama@gmail.com',
            'password': '1234',
        },
    )

    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'username': 'Samael',
        'email': 'sama@gmail.com',
        'id': 1,
    }


# Exercício Aula 5 - Escrever um teste para o endpoint de POST (
# create_user) que contemple o cenário onde o username já foi
# registrado. Validando o erro 400;
def test_create_user_username_exist(client, user):
    """
    Teste para o endpoint de criação de usuário quando o nome de
    usuário já existe.

    Este teste verifica se a API retorna o status HTTP 400 (Bad
    Request) quando tentamos criar um novo usuário com um nome de
    usuário já existente.

    O teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste e
       adiciona um usuário com um nome de usuário específico ao
       banco de dados.
    2. Act (Ação): Faz uma requisição POST para o endpoint de
       criação de usuário com o mesmo nome de usuário.
    3. Assert (Garantia): Verifica se o status da resposta é 400
       Bad Request, indicando que a criação do usuário falhou
       devido a um nome de usuário duplicado.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.
        user (User): Um usuário já existente no banco de dados.

    Raises:
        AssertionError: Se o status da resposta não for 400 Bad
        Request.
    """
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'sama@gmail.com',
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


# Exercício Aula 5 - Escrever um teste para o endpoint de POST (
# create_user) que contemple o cenário onde o email já foi
# registrado. Validando o erro 400;
def test_create_user_email_exist(client, user):
    """
    Teste para o endpoint de criação de usuário quando o email de
    usuário já existe.

    Este teste verifica se a API retorna o status HTTP 400 (Bad
    Request) quando tentamos criar um novo usuário com um email de
    já existente.

    O teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste e
       adiciona um usuário com um email de usuário específico ao
       banco de dados.
    2. Act (Ação): Faz uma requisição POST para o endpoint de
       criação de usuário com o mesmo nome de usuário.
    3. Assert (Garantia): Verifica se o status da resposta é 400
       Bad Request, indicando que a criação do usuário falhou
       devido a um email de usuário duplicado.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.
        user (User): Um usuário já existente no banco de dados.

    Raises:
        AssertionError: Se o status da resposta não for 400 Bad
        Request.
    """
    response = client.post(
        '/users/',
        json={
            'username': 'sama',
            'email': 'teste@teste.com',
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    """
    Teste para o endpoint de leitura de usuários, que deve retornar
    status HTTP 200 e a lista de usuários.

    O teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste.
    2. Act (Ação): Faz uma requisição GET para o endpoint de leitura
    de usuários.
    3. Assert (Garantia): Verifica se o status da resposta é 200 OK
    e se os dados retornados correspondem ao esperado.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.

    Raises:
        AssertionError: Se o status da resposta não for 200 OK ou
        se os dados retornados não corresponderem ao esperado.
    """
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    """
    Teste para o endpoint de leitura de usuários quando há um usuário
    no banco de dados.

    Este teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste e
       adiciona um usuário ao banco de dados.
    2. Act (Ação): Faz uma requisição GET para o endpoint de leitura
       de usuários.
    3. Assert (Garantia): Verifica se o status da resposta é 200 OK
       e se os dados retornados correspondem ao usuário inserido.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.
        user (User): Um usuário já existente no banco de dados.

    Raises:
        AssertionError: Se o status da resposta não for 200 OK ou
        se os dados retornados não corresponderem ao esperado.
    """
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


# Exercício aula 5 - Implementar o banco de dados para o endpoint
# de listagem por id, criado no exercício 3 da aula 03.
def test_read_user(client, user):
    """
    Teste para o endpoint de leitura de um usuário específico.

    Este teste verifica se o endpoint de leitura de um usuário com
    ID específico retorna os dados corretamente e o status HTTP
    200 (OK).

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.
        user (User): O usuário de teste criado na fixture.

    Raises:
        AssertionError: Se o status da resposta não for 200 OK.
    """
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK


def test_read_user_not_found(client):
    """
    Teste para o endpoint de leitura de um usuário inexistente.

    Este teste verifica se o endpoint de leitura de um usuário
    inexistente retorna o status HTTP 404 (Not Found).

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.

    Raises:
        AssertionError: Se o status da resposta não for 404 Not
        Found.
    """
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user, token):
    """
    Teste para o endpoint de atualização de usuário, que deve retornar
    status HTTP 200 e os dados atualizados do usuário.

    Este teste verifica se é possível atualizar um usuário existente
    fazendo uma requisição PUT para o endpoint '/users/{user_id}'.
    Verifica se o status da resposta é 200 OK e se os dados retornados
    correspondem ao usuário atualizado.

    Este teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste e
       adiciona um usuário ao banco de dados.
    2. Act (Ação): Faz uma requisição PUT para o endpoint de
       atualização de usuário.
    3. Assert (Garantia): Verifica se o status da resposta é 200 OK
       e se os dados retornados correspondem ao usuário atualizado.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.
        user (User): Um usuário já existente no banco de dados.
        token (str): O token de acesso JWT para autenticação.

    Raises:
        AssertionError: Se os dados retornados não corresponderem ao
        esperado.
    """
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Samael',
            'email': 'samael@gmail.com',
            'id': user.id,
            'password': '1234',
        },
    )

    assert response.json() == {
        'username': 'Samael',
        'email': 'samael@gmail.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    """
    Teste para o endpoint de exclusão de usuário, que deve retornar
    status HTTP 200 e uma mensagem de confirmação.

    Este teste verifica se é possível deletar um usuário existente
    fazendo uma requisição DELETE para o endpoint '/users/{user_id}'.
    Verifica se o status da resposta é 200 OK e se a mensagem de
    confirmação é retornada.

    Este teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste e
       adiciona um usuário ao banco de dados.
    2. Act (Ação): Faz uma requisição DELETE para o endpoint de
       exclusão de usuário.
    3. Assert (Garantia): Verifica se o status da resposta é 200 OK
       e se a mensagem de confirmação é retornada.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.
        user (User): Um usuário já existente no banco de dados.
        token (str): O token de acesso JWT para autenticação.

    Raises:
        AssertionError: Se os dados retornados não corresponderem ao
        esperado.
    """
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.json() == {'message': 'Usuário deletado'}


def test_get_token(client, user):
    """
    Teste para obter um token de acesso válido.

    Este teste verifica se é possível obter um token de acesso
    válido ao fazer uma requisição POST para o endpoint de login
    '/token'. Verifica se o status da resposta é 200 OK, se o tipo
    de token é 'Bearer' e se o campo 'access_token' está presente
    na resposta.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.
        user (User): Um usuário válido no banco de dados.

    Raises:
        AssertionError: Se os dados retornados não corresponderem ao
        esperado.
    """
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
