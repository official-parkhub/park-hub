from logging.config import fileConfig

import alembic_postgresql_enum
from sqlalchemy import engine_from_config, pool, text

from alembic import context
from src.core.database.base import Base
from src.modules import models
from src.settings import SETTINGS

config = context.config
config.set_main_option(
    "sqlalchemy.url",
    SETTINGS.sqlalchemy_url.replace("%", "%%"),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
assert models, "models must be imported to register the models with SQLAlchemy"

alembic_postgresql_enum.set_configuration(alembic_postgresql_enum.Config(add_type_ignore=True))


def include_object(object, name, type_, reflected, compare_to):
    return not name.startswith("mv_")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.get_context()._ensure_version_table()
            connection.execute(text("LOCK TABLE alembic_version IN ACCESS EXCLUSIVE MODE"))
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
