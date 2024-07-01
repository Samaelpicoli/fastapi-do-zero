from sqlalchemy import select

from fastapi_do_zero.models import User


def test_create_user(session):
    """
    Testa a criação de um usuário no banco de dados.

    Este teste cria um novo usuário, adiciona-o à sessão,
    faz o commit das mudanças e verifica se o usuário foi
    corretamente inserido no banco de dados ao buscar pelo
    email do usuário.

    Args:
        session (Session): A sessão de banco de dados
        fornecida pela fixture.
    """
    user = User(username='Sama', password='rafa', email='sama@gmail.com')
    session.add(user)
    session.commit()

    # Realiza uma consulta para selecionar o usuário com o email
    # especificado
    result = session.scalar(select(User).where(User.email == 'sama@gmail.com'))

    assert result.username == 'Sama'
