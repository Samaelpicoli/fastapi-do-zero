from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fastapi_do_zero.database import get_session
from fastapi_do_zero.models import User
from fastapi_do_zero.settings import Settings

# Configuração do gerador de hash de senha recomendado
pwd_context = PasswordHash.recommended()

# Esquema de autenticação OAuth2 com token de senha
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

# Instânciando o settings para utilização no arquivo
settings = Settings()


def get_password_hash(password: str):
    """
    Gera um hash para a senha fornecida.

    Args:
        password (str): A senha em texto limpo.

    Returns:
        str: A senha criptografada.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Verifica se a senha em texto plano corresponde ao hash.

    Args:
        plain_password (str): A senha em texto plano.
        hashed_password (str): O hash da senha.

    Returns:
        bool: True se as senhas corresponderem, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """
    Cria um token de acesso JWT.

    Args:
        data (dict): Os dados a serem codificados no token.

    Returns:
        str: O token JWT.
    """
    to_encode = data.copy()

    # Configura o tempo de expiração do token
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    # Codifica o token JWT com a chave secreta
    encode_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encode_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    """
    Obtém o usuário atual a partir do token de acesso.

    Args:
        session (Session): Sessão do banco de dados.
        token (str): Token de acesso JWT.

    Raises:
        HTTPException: Se o token não for válido ou o usuário
        não for encontrado.

    Returns:
        User: O usuário autenticado.
    """
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.username == username))

    if not user:
        raise credentials_exception

    return user
