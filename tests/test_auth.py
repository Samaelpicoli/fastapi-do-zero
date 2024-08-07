from http import HTTPStatus

from freezegun import freeze_time


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
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_update_user_not_found_token(client, user, token):
    """
    Teste para o cenário onde o usuário não é encontrado ao tentar
    atualizar os dados do usuário.

    Este teste verifica se o endpoint de atualização de usuário
    retorna o status HTTP 401 (Unauthorized) e a mensagem de erro
    correta quando o usuário autenticado tenta atualizar seus dados
    após ser excluído.

    Este teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste,
       adiciona um usuário ao banco de dados e obtém um token
       de autenticação.
    2. Act (Ação): Exclui o usuário e tenta atualizar os dados do
       usuário com o token de autenticação obtido anteriormente.
    3. Assert (Garantia): Verifica se o status da resposta é 401
       (Unauthorized) e se a mensagem de erro é 'Could not validate
       credentials'.

    Args:
        client (TestClient): O cliente de teste para fazer a requisição.
        user (User): Um usuário já existente no banco de dados.
        token (str): O token de autenticação para o usuário.

    Raises:
        AssertionError: Se os dados retornados não corresponderem
        ao esperado.
    """
    client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    response = client.put(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '123',
            'username': 'sama',
            'email': 'testeteste@gmail.com',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_expired_after_time(client, user):
    """
    Testa a expiração do token após um determinado período de tempo.

    Este teste verifica se o token de acesso expira corretamente
    após 30 minutos. Primeiro, gera um token às 12:00 e depois
    tenta usá-lo às 12:31, esperando que o token seja considerado
    inválido.

    Args:
        client (TestClient): O cliente de teste para fazer a requisição.
        user (User): Um usuário já existente no banco de dados.

    Raises:
        AssertionError: Se o token não expirar corretamente.
    """
    with freeze_time('2023-07-14 12:00:00'):
        # Gerar o token as 12h
        response = client.post(
            '/auth/token',
            data={'username': user.username, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        # Usar o token simulando a passagem dos 30 minutos
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_wrong_password(client, user):
    """
    Testa o login com senha incorreta.

    Este teste verifica se o sistema retorna o código de status
    correto e a mensagem apropriada ao tentar fazer login com uma
    senha incorreta.

    Args:
        client (TestClient): O cliente de teste para fazer a requisição.
        user (User): Um usuário já existente no banco de dados.

    Raises:
        AssertionError: Se o sistema não retornar o código de status
        e a mensagem esperados.
    """
    response = client.post(
        '/auth/token', data={'username': user.username, 'password': '1234'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_token_wrong_username(client, user):
    """
    Testa o login com nome de usuário incorreto.

    Este teste verifica se o sistema retorna o código de status
    correto e a mensagem apropriada ao tentar fazer login com um
    nome de usuário incorreto.

    Args:
        client (TestClient): O cliente de teste para fazer a requisição.
        user (User): Um usuário já existente no banco de dados.

    Raises:
        AssertionError: Se o sistema não retornar o código de status
        e a mensagem esperados.
    """
    response = client.post(
        '/auth/token',
        data={'username': 'blah', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_refresh_token(client, token):
    """
    Testa o endpoint de atualização do token.

    Este teste verifica se o endpoint de atualização do token retorna
    um novo token de acesso e o tipo de token correto.

    Args:
        client (TestClient): O cliente de teste para fazer a requisição.
        token (str): Um token de acesso válido.

    Raises:
        AssertionError: Se o sistema não retornar o código de status
        e os dados esperados.
    """
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    """
    Testa a não atualização de um token expirado.

    Este teste verifica se o sistema não permite a atualização de
    um token de acesso expirado. Primeiro, gera um token às 12:00 e
    depois tenta atualizá-lo às 12:31, esperando que a atualização
    falhe.

    Args:
        client (TestClient): O cliente de teste para fazer a requisição.
        user (User): Um usuário já existente no banco de dados.

    Raises:
        AssertionError: Se o sistema permitir a atualização do token
        expirado.
    """
    with freeze_time('2023-07-14 12:00:00'):
        # Gerar o token as 12h
        response = client.post(
            '/auth/token',
            data={'username': user.username, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        # Usar o token simulando a passagem dos 30 minutos
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
