"""initial schema

Revision ID: 000000000001
Revises:
Create Date: 2026-02-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "000000000001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_buildings_name"), "buildings", ["name"], unique=True)

    op.create_table(
        "floors",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.Column("floor_number", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("building_id", "floor_number", name="uq_floor_building_number"),
    )

    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("floor_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["floor_id"], ["floors.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("floor_id", "name", name="uq_room_floor_name"),
    )

    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("reservation_id", sa.String(length=100), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.Column("floor_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("user_name", sa.String(length=100), nullable=False),
        sa.Column("purpose", sa.String(length=200), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("start_datetime", sa.DateTime(), nullable=False),
        sa.Column("end_datetime", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"]),
        sa.ForeignKeyConstraint(["floor_id"], ["floors.id"]),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reservations_reservation_id"), "reservations", ["reservation_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_reservations_reservation_id"), table_name="reservations")
    op.drop_table("reservations")
    op.drop_table("rooms")
    op.drop_table("floors")
    op.drop_index(op.f("ix_buildings_name"), table_name="buildings")
    op.drop_table("buildings")
