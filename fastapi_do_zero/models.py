from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

# Cria uma instância do registry que é utilizada para mapear
# classes de modelo para tabelas no banco de dados. O registry
# gerencia o mapeamento ORM entre as classes Python e as
# tabelas do banco de dados.
table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    """
    Modelo de dados para a tabela de usuários.

    Esta classe define a estrutura da tabela 'users' no banco de dados,
    utilizando SQLAlchemy para mapeamento objeto-relacional (ORM).
    Cada instância desta classe representa um registro na tabela
    'users'.

    Attributes:
        id (int): Identificador único do usuário (chave primária).
        username (str): Nome de usuário, deve ser único.
        password (str): Senha do usuário.
        email (str): Endereço de email do usuário, deve ser único.
        created_at (datetime): Timestamp da criação do registro,
        definido automaticamente pelo servidor.
    """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    # Exercício aula 4 - Fazer uma alteração no modelo (tabela User)
    # e adicionar um campo chamado updated_at
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
