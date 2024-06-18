from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de Olá Mundo.

    Returns:
        dict: Uma mensagem de Olá Mundo irá aparecer no browser.
    """
    return {'message': 'Olá Mundo!'}
