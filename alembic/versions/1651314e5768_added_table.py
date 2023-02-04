"""Added table

Revision ID: 1651314e5768
Revises: 
Create Date: 2023-02-04 11:44:42.358559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1651314e5768'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ambulance_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.VARCHAR(length=50), nullable=True),
    sa.Column('long', sa.VARCHAR(length=50), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.VARCHAR(length=20), nullable=True),
    sa.Column('lat', sa.Float(precision=50), nullable=True),
    sa.Column('long', sa.Float(precision=50), nullable=True),
    sa.Column('phone_no', sa.Integer(), nullable=True),
    sa.Column('message', sa.TEXT(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('assigned_amb', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assigned_amb'], ['ambulance_data.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('ambulance_data')
    # ### end Alembic commands ###
