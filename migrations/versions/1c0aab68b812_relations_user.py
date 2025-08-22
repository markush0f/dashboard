"""relations-user

Revision ID: 1c0aab68b812
Revises: 9a9a0507cb8d
Create Date: 2025-08-19 17:15:06.415824
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1c0aab68b812"
down_revision: Union[str, Sequence[str], None] = "9a9a0507cb8d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _fk_exists(table: str, name: str) -> bool:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    try:
        fks = insp.get_foreign_keys(table)
    except Exception:
        return False
    return any(fk.get("name") == name for fk in fks)


def _index_exists(table: str, name: str) -> bool:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    try:
        idxs = insp.get_indexes(table)
    except Exception:
        return False
    return any(ix.get("name") == name for ix in idxs)


def _table_exists(name: str) -> bool:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    return name in insp.get_table_names()


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # 1) Renombrar tabla users -> user si existe; si no existe ninguna, crear user
    has_users = _table_exists("users")
    has_user = _table_exists("user")

    if has_users and not has_user:
        op.rename_table("users", "user")
    elif not has_users and not has_user:
        # Crear tabla user desde cero
        op.create_table(
            "user",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("email", sa.String(length=320), nullable=False),
            sa.Column("full_name", sa.String(length=255), nullable=False),
            sa.Column("disabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
            sa.PrimaryKeyConstraint("id"),
        )

    # 2) Índices: asegurar ix_user_email único, y eliminar ix_users_email si quedó
    if _index_exists("users", op.f("ix_users_email")):
        op.drop_index(op.f("ix_users_email"), table_name="users")
    # ix_user_email puede no existir tras rename; créalo si falta
    if not _index_exists("user", op.f("ix_user_email")):
        op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)

    # 3) Foreign Key en event.user_id: apuntar a user.id (y no a users.id)
    # Drop FK antigua si existe
    old_fk = op.f("fk_event_user_id__users_id")
    if _fk_exists("event", old_fk):
        op.drop_constraint(old_fk, "event", type_="foreignkey")

    # Crear FK nueva si no existe ya alguna a user.id
    new_fk = op.f("fk_event_user_id__user_id")
    if not _fk_exists("event", new_fk):
        op.create_foreign_key(
            new_fk,
            source_table="event",
            referent_table="user",
            local_cols=["user_id"],
            remote_cols=["id"],
            ondelete="CASCADE",  # quita esto si no quieres cascada real
        )


def downgrade() -> None:
    """Downgrade schema."""
    # 1) Cambiar FK para que vuelva a users.id
    new_fk = op.f("fk_event_user_id__user_id")
    if _fk_exists("event", new_fk):
        op.drop_constraint(new_fk, "event", type_="foreignkey")
    old_fk = op.f("fk_event_user_id__users_id")
    if not _fk_exists("event", old_fk) and _table_exists("users"):
        op.create_foreign_key(
            old_fk,
            source_table="event",
            referent_table="users",
            local_cols=["user_id"],
            remote_cols=["id"],
            ondelete="CASCADE",
        )

    # 2) Índices
    if _index_exists("user", op.f("ix_user_email")):
        op.drop_index(op.f("ix_user_email"), table_name="user")

    if _table_exists("users"):
        if not _index_exists("users", op.f("ix_users_email")):
            op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    # 3) Tabla: renombrar user -> users si users no existe; si users ya existe, borrar user
    has_users = _table_exists("users")
    has_user = _table_exists("user")
    if has_user and not has_users:
        op.rename_table("user", "users")
    elif has_user and has_users:
        # Situación rara: ambas existen; conservamos users y eliminamos user
        op.drop_table("user")
