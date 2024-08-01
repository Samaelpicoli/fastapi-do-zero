from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
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


class TodoState(str, Enum):
    """
    Enumeração para representar os diferentes estados de uma tarefa.

    Attributes:
        draft (str): Representa um rascunho de tarefa.
        todo (str): Representa uma tarefa a ser feita.
        doing (str): Representa uma tarefa em andamento.
        done (str): Representa uma tarefa concluída.
        trash (str): Representa uma tarefa descartada.
    """

    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class Todo:
    """
    Modelo para representar uma tarefa.

    Attributes:
        id (int): Identificador único da tarefa.
        title (str): Título da tarefa.
        description (str): Descrição detalhada da tarefa.
        state (TodoState): Estado atual da tarefa.
        user_id (int): Identificador do usuário ao qual a tarefa pertence.
    """

    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]

    # Exercicios Aula 9
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
