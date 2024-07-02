from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .settings import Settings

# Cria um engine do SQLAlchemy usando a URL de
# banco de dados definida nas configurações
engine = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover
    """
    Obtém uma sessão de banco de dados.

    Esta função cria uma sessão de banco de dados utilizando o
    engine configurado.
    A sessão é gerada como um generator, permitindo que seja
    usada com `yield` em contextos como dependências do FastAPI.

    Yields:
        Session: Uma sessão de banco de dados configurada.
    """
    with Session(engine) as session:
        yield session
