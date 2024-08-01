from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_do_zero.database import get_session
from fastapi_do_zero.models import Todo, User
from fastapi_do_zero.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fastapi_do_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, session: T_Session, user: CurrentUser):
    """
    Endpoint para criar uma nova tarefa.

    Esta função recebe os dados da tarefa através do esquema TodoSchema,
    cria um novo objeto Todo e o salva no banco de dados. O usuário atual
    é obtido a partir do token de autenticação.

    Args:
        todo (TodoSchema): Os dados da nova tarefa.
        session (Session): Sessão de banco de dados.
        user (User): Usuário autenticado.

    Returns:
        TodoPublic: A tarefa criada com os dados públicos.
    """

    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(  # noqa
    session: T_Session,
    user: CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    """
    Endpoint para listar tarefas.

    Esta função permite filtrar as tarefas por título, descrição e estado.
    Os resultados podem ser paginados utilizando os parâmetros offset e limit.

    Args:
        session (Session): Sessão de banco de dados.
        user (User): Usuário autenticado.
        title (str, optional): Filtro pelo título da tarefa.
        description (str, optional): Filtro pela descrição da tarefa.
        state (str, optional): Filtro pelo estado da tarefa.
        offset (int, optional): Número de tarefas a pular (para paginação).
        limit (int, optional): Número máximo de tarefas a retornar.

    Returns:
        TodoList: Uma lista de tarefas que correspondem aos filtros aplicados.
    """

    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: T_Session, user: CurrentUser):
    """
    Endpoint para deletar uma tarefa.

    Este endpoint deleta uma tarefa existente associada ao usuário atual
    e retorna uma mensagem de confirmação.

    Args:
        todo_id (int): O ID da tarefa a ser deletada.
        session (Session): A sessão de banco de dados a ser utilizada.
        user (User): O usuário atualmente autenticado.

    Raises:
        HTTPException: Se a tarefa não for encontrada.

    Returns:
        Message: Uma mensagem de confirmação da exclusão.
    """

    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int,
    session: T_Session,
    user: CurrentUser,
    todo: TodoUpdate,
):
    """
    Endpoint para atualizar parcialmente uma tarefa.

    Este endpoint permite a atualização parcial de uma tarefa existente
    associada ao usuário atual. Apenas os campos fornecidos no corpo da
    requisição serão atualizados.

    Args:
        todo_id (int): O ID da tarefa a ser atualizada.
        session (Session): A sessão de banco de dados a ser utilizada.
        user (User): O usuário atualmente autenticado.
        todo (TodoUpdate): O objeto com os dados da tarefa a serem atualizados.

    Raises:
        HTTPException: Se a tarefa não for encontrada.

    Returns:
        TodoPublic: A tarefa atualizada.
    """
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
