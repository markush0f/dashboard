# Cambio: integrar SQLModel + settings del proyecto
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
import os, sys

# Cambio: añadir app al sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# Cambio: importar settings y modelos
from app.core.config import settings
from app.domain.events import models as events_models
from app.domain.goals import models as goals_models

config = context.config

# Cambio: inyectar DATABASE_URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Cambio: usar metadatos de SQLModel
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    url = settings.DATABASE_URL  # Cambio
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,            # Cambio
        compare_server_default=True,  # Cambio
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,            # Cambio
            compare_server_default=True,  # Cambio
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
