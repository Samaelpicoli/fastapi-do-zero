from http import HTTPStatus


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
