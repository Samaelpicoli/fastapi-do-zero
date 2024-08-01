from http import HTTPStatus

from fastapi import FastAPI

from fastapi_do_zero.routers import auth, todo, users
from fastapi_do_zero.schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de Olá Mundo.
    Este endpoint responde com uma mensagem de 'Olá Mundo' quando
    acessado. O código de status HTTP retornado é 200 (OK).

    Returns:
        dict: Uma mensagem de Olá Mundo.
    """
    return {'message': 'Olá Mundo!'}
