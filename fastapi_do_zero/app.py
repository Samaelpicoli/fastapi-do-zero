from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from .schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()


database = []  # banco falso e provisório para estudo (é uma lista)


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


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    """
    Endpoint para criar um novo usuário.

    Este endpoint recebe os dados de um usuário e retorna as
    informações públicas do usuário criado. Os dados do usuário
    são validados de acordo com o esquema definido em UserSchema.
    O código de status HTTP retornado é 201 (Created).

    Args:
        user (UserSchema): Um objeto contendo os dados do usuário.

    Returns:
        UserPublic: Um objeto contendo as informações públicas do
        usuário. De acordo com o esquema definido em UserPublic.
    """
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList)
def read_users():
    """
    Endpoint para listar todos os usuários.

    Este endpoint retorna uma lista de todos os usuários cadastrados.
    O código de status HTTP retornado é 200 (OK).

    Returns:
        UserList: Um objeto contendo uma lista de usuários.
        De acordo com o esquema definido em UserList.
    """
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    """
    Endpoint para atualizar um usuário existente.

    Este endpoint recebe os novos dados de um usuário e atualiza
    as informações do usuário correspondente ao ID fornecido. Os
    dados do usuário são validados de acordo com o esquema definido
    em UserSchema.
    O código de status HTTP retornado é 200 (OK).

    Args:
        user_id (int): O ID do usuário a ser atualizado.
        user (UserSchema): Um objeto contendo os novos dados
        do usuário.

    Raises:
        HTTPException: Se o usuário com o ID fornecido não
        for encontrado.

    Returns:
        UserPublic: Um objeto contendo as informações públicas
        do usuário atualizado.
        De acordo com o esquema definido em UserPublic.

    """
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    """
    Endpoint para deletar um usuário.

    Este endpoint deleta o usuário correspondente ao ID fornecido.
    O código de status HTTP retornado é 200 (OK).

    Args:
        user_id (int): O ID do usuário a ser deletado.

    Raises:
        HTTPException: Se o usuário com o ID fornecido não
        for encontrado.

    Returns:
        Message: Uma mensagem confirmando a deleção do usuário.
        De acordo com o esquema definido em Message.
    """
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
