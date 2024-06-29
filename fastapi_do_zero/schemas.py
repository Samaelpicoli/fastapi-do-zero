from pydantic import BaseModel, EmailStr


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


class UserDB(UserSchema):
    """
    Schema para os dados do usuário no banco de dados.

    Este modelo herda de UserSchema e adiciona o atributo id,
    representando a estrutura completa de um usuário armazenado
    no banco de dados.

    Attributes:
        id (int): Identificador único do usuário.
    """

    id: int


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
    """

    id: int
    username: str
    email: EmailStr


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
