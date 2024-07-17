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
