from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de Olá Mundo.
    Se tudo ocorrer corretamente irá retornar o
    status_code como HTTPStatus.OK. Por padrão o FastAPI
    retorna o status do verbo get como 200.

    Returns:
        dict: Uma mensagem de Olá Mundo irá aparecer no browser.
    """
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""
