
"""Migracion inicial de videojuegos

Revision ID: e287c0146427
Revises:
Create Date: 2026-10-16 17:38:48.894648
"""

from alembic import op
import sqlalchemy as sa

# Identificadores de la migracion
revision = 'e287c0146427'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # La tabla juegos ya existe en MySQL.
    # No es necesario modificar su estructura.
    pass


def downgrade():
    # No eliminamos la tabla para conservar los datos.
    pass
