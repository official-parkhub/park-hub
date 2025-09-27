from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.path import ROOT_DIR

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True)
    # API
    api_version: str
    api_reload: bool = False
    api_port: int = 80
    api_host: str = "0.0.0.0"

    # Optional Features
    feat_enable_core_docs: bool = True
    feat_allow_wildcard_cors: bool = False

    # Auth
    auth_secret_key: str

    # Postgres
    postgres_user: str
    postgres_password: str
    postgres_database: str
    postgres_host: str
    postgres_port: int = 5432

    # SQLAlchemy
    sqlalchemy_echo: bool = False

    @property
    def sqlalchemy_url(self):
        user = quote_plus(self.postgres_user)
        password = quote_plus(self.postgres_password)
        database = self.postgres_database
        host = self.postgres_host
        port = self.postgres_port
        return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"

ENV_FILE = ROOT_DIR / "env/.env"
SETTINGS = Settings(_env_file=ENV_FILE)
