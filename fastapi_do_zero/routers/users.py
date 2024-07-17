from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_do_zero.database import get_session
from fastapi_do_zero.models import User
from fastapi_do_zero.schemas import Message, UserList, UserPublic, UserSchema
from fastapi_do_zero.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=UserList)
def read_users(session: T_Session, limit: int = 10, skip: int = 0):
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


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: T_Session):
    """
    Endpoint para ler os dados de um usuário específico.

    Este endpoint retorna as informações públicas de um usuário
    com base no ID fornecido. Se o usuário não for encontrado, é
    retornado um erro 404 (Not Found).

    Args:
        user_id (int): O identificador do usuário.
        session (Session): A sessão do banco de dados.

    Returns:
        UserPublic: Um objeto contendo as informações públicas do
        usuário.

    Raises:
        HTTPException: Se o usuário com o ID fornecido não for
        encontrado, uma exceção HTTP 404 é levantada com a mensagem
        "Usuário não existe".

    Exercicío Aula 3 - Criar um endpoint de GET para pegar um único
    recurso como users/{id} e fazer seus testes.
    Exercício aula 5 - Implementar o banco de dados para o endpoint
    de listagem por id, criado no exercício 3 da aula 03.
    """
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe'
        )

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
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
        current_user (User): O usuário atualmente autenticado, obtido
        a partir do token de autenticação.

    Raises:
        HTTPException: Se o usuário não existir ou se o usuário
        autenticado não tiver permissão.

    Returns:
        UserPublic: Um objeto contendo as informações públicas do
        usuário.De acordo com o esquema definido em UserPublic.
    """
    # Verifica se o usuário autenticado tem permissão para atualizar o usuário
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: T_Session, current_user: T_CurrentUser):
    """
    Endpoint para deletar um usuário.

    Este endpoint deleta um usuário existente e retorna uma mensagem
    de confirmação. O código de status HTTP retornado é 200 (OK).

    Args:
        user_id (int): O ID do usuário a ser deletado.
        session (Session): A sessão de banco de dados a ser utilizada.
        current_user (User): O usuário atualmente autenticado, obtido
        a partir do token de autenticação.

    Raises:
        HTTPException: Se o usuário não existir ou se o usuário
        autenticado não tiver permissão.

    Returns:
        Message: Uma mensagem de confirmação da exclusão.
    """
    # Verifica se o usuário autenticado tem permissão para deletar o usuário
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Usuário deletado'}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
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
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
