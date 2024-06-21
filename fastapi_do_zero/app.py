from http import HTTPStatus

from fastapi import FastAPI

from .schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de Olá Mundo.
    Se tudo ocorrer corretamente irá retornar o
    status_code como HTTPStatus.OK. Por padrão o FastAPI
    retorna o status do verbo get como 200.

    Returns:
        dict: Uma mensagem de Olá Mundo irá aparecer no browser.
    """
    return {'message': 'Olá Mundo!'}
