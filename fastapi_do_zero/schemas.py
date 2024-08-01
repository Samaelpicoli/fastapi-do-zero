from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from fastapi_do_zero.models import TodoState


class Message(BaseModel):
    """
    Schema para mensagens de resposta.

    Este modelo é usado para definir o formato das
    mensagens de resposta que a API retornará.

    Attributes:
        message (str): O conteúdo da mensagem.
    """

    message: str


class UserSchema(BaseModel):
    """
    Schema para os dados do usuário.

    Este modelo define a estrutura dos dados necessários
    para criar ou atualizar um usuário no sistema.

    Attributes:
        username (str): O nome de usuário.
        email (EmailStr): O endereço de email do usuário.
        password (str): A senha do usuário.
    """

    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """
    Schema para os dados públicos do usuário.

    Este modelo define a estrutura dos dados que serão expostos
    publicamente sobre um usuário. Usado para exibir
    informações de perfil sem revelar a senha.

    Attributes:
        id (int): Identificador do usuário.
        username (str): O nome de usuário.
        email (EmailStr): O endereço de email do usuário.
        Deve ser um email válido.
        model_config (ConfigDict): Configuração adicional para o
        modelo Pydantic. Utiliza 'from_attributes=True' para permitir
        a criação do modelo a partir de instâncias de classes que
        possuam atributos correspondentes.
    """

    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserList(BaseModel):
    """
    Schema para a lista de usuários.

    Este modelo define a estrutura de uma lista de usuários,
    onde cada usuário é representado pelos dados públicos definidos
    no modelo UserPublic.

    Attributes:
        users (list[UserPublic]): A lista de usuários.
    """

    users: list[UserPublic]


class Token(BaseModel):
    """
    Schema para o token de acesso.

    Este modelo define a estrutura dos dados do token de acesso
    retornado após a autenticação do usuário.

    Attributes:
        access_token (str): O token de acesso JWT.
        token_type (str): O tipo do token, geralmente 'bearer'.
    """

    access_token: str
    token_type: str


class TodoSchema(BaseModel):
    """
    Esquema de validação para criação e atualização de tarefas.

    Attributes:
        title (str): O título da tarefa.
        description (str): A descrição detalhada da tarefa.
        state (TodoState): O estado atual da tarefa.
    """

    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    """
    Esquema para representar uma tarefa pública.

    Attributes:
        id (int): O identificador único da tarefa.
    """

    id: int
    created_at: datetime
    updated_at: datetime | None = None


class TodoList(BaseModel):
    """
    Esquema para representar uma lista de tarefas públicas.

    Attributes:
        todos (list[TodoPublic]): Uma lista de tarefas públicas.
    """

    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    """
    Esquema para atualizar parcialmente uma tarefa.

    Todos os campos são opcionais. Apenas os campos fornecidos serão
    atualizados.

    Args:
        title (str | None): Novo título da tarefa.
        description (str | None): Nova descrição da tarefa.
        state (TodoState | None): Novo estado da tarefa.
    """

    title: str | None = None
