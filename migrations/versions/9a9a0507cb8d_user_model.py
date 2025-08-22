"""user model

Revision ID: 9a9a0507cb8d
Revises: fe50dc61df5d
Create Date: 2025-08-19 17:05:12.309752
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9a9a0507cb8d"
down_revision: Union[str, Sequence[str], None] = "fe50dc61df5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- Tabla users (evitar palabra reservada "user") ---
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column(
            "disabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    # --- Eliminar goals si existe (más seguro que drop_table directo) ---
    op.execute("DROP TABLE IF EXISTS goals")

    # --- Columna de relación en event ---
    # Primero nullable=True para no romper datos existentes
    op.add_column("event", sa.Column("user_id", sa.Integer(), nullable=True))

    # Índice no único sobre la FK
    op.create_index(op.f("ix_event_user_id"), "event", ["user_id"], unique=False)

    # Clave foránea a users.id
    op.create_foreign_key(
        "fk_event_user_id__users_id", "event", "users", ["user_id"], ["id"]
    )

    # Si necesitas que sea NOT NULL, aquí deberías backfillear y luego:
    # op.execute("UPDATE event SET user_id = <valor_por_defecto> WHERE user_id IS NULL")
    # op.alter_column("event", "user_id", existing_type=sa.Integer(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Revertir FK e índice en event
    op.drop_constraint("fk_event_user_id__users_id", "event", type_="foreignkey")
    op.drop_index(op.f("ix_event_user_id"), table_name="event")
    op.drop_column("event", "user_id")

    # Restaurar tabla goals mínima (ajusta columnas si tu esquema original tenía más)
    op.create_table(
        "goals",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("goals_pkey")),
    )

    # Quitar índice y tabla users
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
