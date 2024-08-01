from datetime import UTC, datetime
from http import HTTPStatus

from fastapi_do_zero.models import TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token):
    """
    Testa a criação de uma nova tarefa.

    Verifica se a tarefa é criada corretamente e se o
    JSON de resposta contém os dados esperados.
    """
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )

    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
        'created_at': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S'),
        'updated_at': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S'),
    }


def test_list_todos_should_return_5_todos(session, client, user, token):
    """
    Testa a listagem de tarefas.

    Verifica se o endpoint retorna 5 tarefas quando 5 tarefas
    são criadas no banco de dados.
    """
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['todos']) == expected_todos
    assert response.json()['todos'][1]['created_at'] is not None
    assert response.json()['todos'][1]['updated_at'] is not None


def test_list_todos_pagination_should_return_2_todos(
    session, user, client, token
):
    """
    Testa a paginação na listagem de tarefas.

    Verifica se o endpoint retorna 2 tarefas quando a paginação é
    usada com offset 1 e limit 2.
    """
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos
    assert response.json()['todos'][1]['created_at'] is not None
    assert response.json()['todos'][1]['updated_at'] is not None


def test_list_todos_filter_tile_should_return_5_todos(
    session, user, client, token
):
    """
    Testa o filtro por título na listagem de tarefas.

    Verifica se o endpoint retorna 5 tarefas quando o filtro de
    título é aplicado.
    """
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos
    assert response.json()['todos'][1]['created_at'] is not None
    assert response.json()['todos'][1]['updated_at'] is not None


def test_list_todos_filter_description_should_return_5_todos(
    session, user, client, token
):
    """
    Testa o filtro por descrição na listagem de tarefas.

    Verifica se o endpoint retorna 5 tarefas quando o
    filtro de descrição é aplicado.
    """
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description='Test 1')
    )
    session.commit()

    response = client.get(
        '/todos/?description=Tes',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos
    assert response.json()['todos'][1]['created_at'] is not None
    assert response.json()['todos'][1]['updated_at'] is not None


def test_list_todos_filter_state_should_return_5_todos(
    session, user, client, token
):
    """
    Testa o filtro por estado na listagem de tarefas.

    Verifica se o endpoint retorna 5 tarefas quando o filtro
    de estado é aplicado.
    """
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.trash)
    )
    session.commit()

    response = client.get(
        '/todos/?state=trash',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos
    assert response.json()['todos'][1]['created_at'] is not None
    assert response.json()['todos'][1]['updated_at'] is not None


def test_list_todos_filter_combined_should_return_5_todos(
    session, user, client, token
):
    """
    Testa filtros combinados na listagem de tarefas.

    Verifica se o endpoint retorna 5 tarefas quando filtros de título,
    descrição e estado são aplicados em conjunto.
    """
    expected_todos = 5

    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos
    assert response.json()['todos'][1]['created_at'] is not None
    assert response.json()['todos'][1]['updated_at'] is not None


def test_delete_todo(session, client, user, token):
    """
    Testa a exclusão de uma tarefa.

    Verifica se uma tarefa é excluída com sucesso e se a
    resposta contém a mensagem de sucesso.
    """
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_todo_error(client, token):
    """
    Testa a exclusão de uma tarefa inexistente.

    Verifica se o endpoint retorna um erro 404 quando
    a tarefa não é encontrada.
    """
    response = client.delete(
        f'/todos/{8}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_patch_todo(session, client, user, token):
    """
    Testa a atualização parcial de uma tarefa.

    Verifica se a tarefa é atualizada corretamente e se o
    título é alterado.
    """
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste3'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json()['title'] == 'teste3'
    assert response.json()['created_at'] is not None
    assert response.json()['updated_at'] is not None


def test_patch_todo_error(client, token):
    """
    Testa a atualização parcial de uma tarefa inexistente.

    Verifica se o endpoint retorna um erro 404 quando a tarefa não é
    encontrada.
    """
    response = client.patch(
        f'/todos/{8}',
        json={'title': 'teste3'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
