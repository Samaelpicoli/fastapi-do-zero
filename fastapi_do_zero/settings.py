from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação.

    Esta classe utiliza Pydantic BaseSettings para gerenciar
    as configurações da aplicação a partir de variáveis de ambiente.
    A configuração é lida de um arquivo `.env` codificado em UTF-8.

    Attributes:
        model_config (SettingsConfigDict): Configuração do Pydantic
        para leitura do arquivo de ambiente e seu encoding.
        Ele faz a leitura de um arquivo .env.
        DATABASE_URL (str): URL de conexão com o banco de dados.
        Obtida do arquivo .env.
    """

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str
