from http import HTTPStatus


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


# Exercicío Aula 3 - Criar um endpoint de GET para pegar um único
# recurso como users/{id} e fazer seus testes.
def test_read_user(client):
    """
    Testa o endpoint de leitura de um usuário específico para
    verificar se retorna
    o status HTTP 200 (OK) e as informações públicas do usuário.

    Args:
        client (TestClient): O cliente de teste FastAPI.

    Asserts:
        Verifica se o status code da resposta é 200 (OK).
        Verifica se o JSON da resposta contém as informações
        públicas do usuário.
    """
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'username': 'Samael',
        'email': 'sama@gmail.com',
        'id': 1,
    }


def test_read_user_not_found(client):
    """
    Testa o endpoint de leitura de um usuário específico para
    verificar se retorna
    o status HTTP 404 (Not Found) quando o usuário não é encontrado.

    Args:
        client (TestClient): O cliente de teste FastAPI.

    Asserts:
        Verifica se o status code da resposta é 404 (Not Found).
    """
    response = client.get('/users/3')
    assert response.status_code == HTTPStatus.NOT_FOUND


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
    assert response.json() == {
        'users': [
            {
                'username': 'Samael',
                'email': 'sama@gmail.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    """
    Teste para o endpoint de atualização de usuário, que deve retornar
    status HTTP 200 e os dados atualizados do usuário.

    O teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste.
    2. Act (Ação): Faz uma requisição PUT para o endpoint de
    atualização de usuário com os dados atualizados do usuário.
    3. Assert (Garantia): Verifica se os dados retornados
    correspondem ao esperado.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.

    Raises:
        AssertionError: Se os dados retornados não corresponderem
        ao esperado.
    """
    response = client.put(
        '/users/1',
        json={
            'username': 'Samael',
            'email': 'samael@gmail.com',
            'id': 1,
            'password': '1234',
        },
    )

    assert response.json() == {
        'username': 'Samael',
        'email': 'samael@gmail.com',
        'id': 1,
    }


# Exercício Aula 3 - Escrever um teste para o erro de 404
# (NOT FOUND) para o endpoint de PUT;
def test_update_user_not_found(client):
    """
    Testa o endpoint de alteração de um usuário específico para
    verificar se retorna
    o status HTTP 404 (Not Found) quando o usuário não é encontrado.

    Args:
        client (TestClient): O cliente de teste FastAPI.

    Asserts:
        Verifica se o status code da resposta é 404 (Not Found).
    """
    response = client.put(
        '/users/2',
        json={
            'username': 'Samael',
            'email': 'samael@gmail.com',
            'id': 1,
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    """
    Teste para o endpoint de deleção de usuário, que deve retornar
    status HTTP 200 e uma mensagem de confirmação.

    O teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste.
    2. Act (Ação): Faz uma requisição DELETE para o endpoint de deleção
    de usuário.
    3. Assert (Garantia): Verifica se a mensagem retornada corresponde
    ao esperado.

    Args:
        client (TestClient): O cliente de teste para fazer a
        requisição.

    Raises:
        AssertionError: Se a mensagem retornada não corresponder
        ao esperado.
    """
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted'}


# Exercício Aula 3 - Escrever um teste para o erro de 404
# (NOT FOUND) para o endpoint de DELETE;
def test_delete_user_not_found(client):
    """
    Testa o endpoint de exclusão de um usuário específico para
    verificar se retorna
    o status HTTP 404 (Not Found) quando o usuário não é encontrado.

    Args:
        client (TestClient): O cliente de teste FastAPI.

    Asserts:
        Verifica se o status code da resposta é 404 (Not Found).
    """
    response = client.delete('/users/3')
    assert response.status_code == HTTPStatus.NOT_FOUND
