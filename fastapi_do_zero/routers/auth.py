from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_do_zero.database import get_session
from fastapi_do_zero.models import User
from fastapi_do_zero.schemas import Token
from fastapi_do_zero.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token')
def login_for_access_token(session: T_Session, form_data: T_OAuth2Form):
    """
    Endpoint para login e obtenção de token de acesso.

    Este endpoint verifica as credenciais do usuário e, se forem
    válidas, retorna um token de acesso. O código de status HTTP
    retornado é 200 (OK) ou 400 (Bad Request) em caso de falha.

    Args:
        form_data (OAuth2PasswordRequestForm): Os dados do formulário
        de login, contendo o nome de usuário e a senha.
        session (Session): A sessão de banco de dados a ser utilizada.

    Raises:
        HTTPException: Se o nome de usuário ou a senha estiverem
        incorretos.

    Returns:
        dict: Um dicionário contendo o token de acesso e o tipo de
        token.
    """
    # Busca o usuário no banco de dados pelo nome de usuário
    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )
    # Verifica se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect username or password'
        )
    # Cria o token de acesso para o usuário autenticado
    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: User = Depends(get_current_user)):
    """
    Endpoint para atualizar o token de acesso.

    Este endpoint gera um novo token de acesso para o usuário
    autenticado usando o token de acesso anterior. O novo token é
    retornado no formato WT. O código de status HTTP retornado
    é 200 (OK).

    Args:
        user (User): O usuário autenticado, obtido a partir do
        token de acesso atual.

    Returns:
        dict: Um dicionário contendo o novo token de acesso e
        o tipo de token.

    Raises:
        HTTPException: Se as credenciais não puderem ser validadas.
    """
    new_access_token = create_access_token(data={'sub': user.username})
    return {'access_token': new_access_token, 'token_type': 'bearer'}
