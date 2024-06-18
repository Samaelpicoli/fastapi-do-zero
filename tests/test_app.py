from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_do_zero.app import app


def teste_read_root_deve_retornar_ok_e_ola_mundo():
    """
    Teste para o endpoint raiz, que deve retornar status HTTP 200 e a mensagem 'Olá Mundo!'.

    O teste segue três fases:
    1. Arrange (Organização do Teste): Cria o cliente de teste.
    2. Act (Ação): Faz uma requisição GET para o endpoint raiz.
    3. Assert (Garantia): Verifica se o status da resposta é 200 OK
    e se a mensagem retornada é 'Olá Mundo!'.

    Raises:
        AssertionError: Se o status da resposta não for 200 OK ou
        se a mensagem retornada não for 'Olá Mundo!'.
    """

    client = TestClient(app)  # Fase 1: Arrange (Organização do Teste)

    resposta = client.get('/')  # Fase 2: Act (Ação)

    assert (
        resposta.status_code == HTTPStatus.OK
    )  # Fase 3: Assert (Garantia de que dê certo)

    assert resposta.json() == {'message': 'Olá Mundo!'}
