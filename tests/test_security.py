from http import HTTPStatus

from jwt import decode

from fastapi_do_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    """
    Teste para a criação e decodificação de um token JWT.

    Este teste verifica se o token JWT criado contém os dados
    corretos e um campo de expiração.

    Raises:
        AssertionError: Se o token decodificado não contiver os dados
        esperados ou não tiver um campo de expiração.
    """
    # Dados para o token
    data = {'sub': 'test'}
    # Cria o token JWT
    token = create_access_token(data)
    # Decodifica o token JWT
    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    # Verifica se o campo 'sub' no token decodificado é igual
    # ao original
    assert decoded['sub'] == data['sub']

    # Verifica se o token tem um campo de expiração
    assert decoded['exp']


def test_jwt_invalid_token(client):
    """
    Teste para a autenticação com um token JWT inválido.

    Este teste verifica se a API retorna um erro de
    credenciais inválidas ao usar um token JWT inválido.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.

    Raises:
        AssertionError: Se o status da resposta não for 401
        Unauthorized ou se a mensagem de erro não for a esperada.
    """
    # Faz uma requisição DELETE com um token inválido
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    # Verifica se o status da resposta é 401 Unauthorized
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    # Verifica se a mensagem de erro é a esperada
    assert response.json() == {'detail': 'Could not validate credentials'}
