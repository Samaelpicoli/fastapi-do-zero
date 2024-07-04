from pydantic import BaseModel, ConfigDict, EmailStr


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
