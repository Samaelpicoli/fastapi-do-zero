from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_session
from .models import User
from .schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


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
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    """
    Endpoint para criar um novo usuário.

    Este endpoint recebe os dados de um usuário e retorna as
    informações públicas do usuário criado. Os dados do usuário
    são validados de acordo com o esquema definido em UserSchema.
    O código de status HTTP retornado é 201 (Created).

    Args:
        user (UserSchema): Um objeto contendo os dados do usuário.
        session (Session): A sessão de banco de dados a ser utilizada.

    Raises:
        HTTPException: Se o usuário ou e-mail já existirem.

    Returns:
        UserPublic: Um objeto contendo as informações públicas do
        usuário. De acordo com o esquema definido em UserPublic.
    """
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Usuário já existente',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='E-mail já existente',
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    session: Session = Depends(get_session), limit: int = 10, skip: int = 0
):
    """
    Endpoint para listar todos os usuários.

    Este endpoint retorna uma lista de todos os usuários cadastrados.
    O código de status HTTP retornado é 200 (OK).

    Args:
        session (Session): A sessão de banco de dados a ser utilizada.
        limit (int): Número máximo de usuários a serem retornados.
        skip (int): Número de usuários a serem ignorados.

    Returns:
        UserList: Um objeto contendo uma lista de usuários.
        De acordo com o esquema definido em UserList.
    """
    user = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': user}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    """
    Endpoint para atualizar um usuário existente.

    Este endpoint recebe os dados atualizados de um usuário e retorna
    as informações públicas do usuário atualizado. Os dados do usuário
    são validados de acordo com o esquema definido em UserSchema.
    O código de status HTTP retornado é 200 (OK).

    Args:
        user_id (int): O ID do usuário a ser atualizado.
        user (UserSchema): Um objeto contendo os dados atualizados
        do usuário.
        session (Session): A sessão de banco de dados a ser utilizada.

    Raises:
        HTTPException: Se o usuário não existir.

    Returns:
        UserPublic: Um objeto contendo as informações públicas do
        usuário.De acordo com o esquema definido em UserPublic.
    """
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe'
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """
    Endpoint para deletar um usuário.

    Este endpoint deleta um usuário existente e retorna uma mensagem
    de confirmação. O código de status HTTP retornado é 200 (OK).

    Args:
        user_id (int): O ID do usuário a ser deletado.
        session (Session): A sessão de banco de dados a ser utilizada.

    Raises:
        HTTPException: Se o usuário não existir.

    Returns:
        Message: Uma mensagem de confirmação da exclusão.
    """
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'Usuário deletado'}


# Exercicío Aula 3 - Criar um endpoint de GET para pegar um único
# recurso como users/{id} e fazer seus testes.
@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int):
    """
    Endpoint para obter informações de um usuário específico.

    Este endpoint retorna as informações públicas de um usuário
    com base no ID fornecido. O código de status HTTP retornado
    é 200 (OK).

    Args:
        user_id (int): O ID do usuário a ser recuperado.

    Raises:
        HTTPException: Se o usuário com o ID fornecido não for
        encontrado.

    Returns:
        UserPublic: Um objeto contendo as informações públicas
        do usuário. De acordo com o esquema definido em UserPublic.
    """
    ...
