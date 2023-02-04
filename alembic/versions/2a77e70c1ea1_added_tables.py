"""Added tables

Revision ID: 2a77e70c1ea1
Revises: 
Create Date: 2022-11-02 18:12:11.861302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a77e70c1ea1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module_master',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_name', sa.VARCHAR(length=150), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('system_id', sa.Integer(), nullable=True),
    sa.Column('unique_key_1', sa.VARCHAR(length=30), nullable=True),
    sa.Column('unique_key_2', sa.VARCHAR(length=30), nullable=True),
    sa.Column('unique_key_3', sa.VARCHAR(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_master',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_name', sa.String(length=150), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.VARCHAR(length=30), nullable=True),
    sa.Column('parent_event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['module_master.id'], ),
    sa.ForeignKeyConstraint(['parent_event_id'], ['event_master.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('column_master',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_master_id', sa.Integer(), nullable=True),
    sa.Column('column_name', sa.VARCHAR(length=50), nullable=True),
    sa.ForeignKeyConstraint(['event_master_id'], ['event_master.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_analysis_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_master_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('unique_value_1', sa.SmallInteger(), nullable=False),
    sa.Column('unique_value_2', sa.Integer(), nullable=True),
    sa.Column('unique_value_3', sa.VARCHAR(length=30), nullable=True),
    sa.Column('extra_meta_data', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['event_master_id'], ['event_master.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meta_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('column_master_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.VARCHAR(length=30), nullable=True),
    sa.Column('event_analysis_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['column_master_id'], ['column_master.id'], ),
    sa.ForeignKeyConstraint(['event_analysis_id'], ['event_analysis_details.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meta_data')
    op.drop_table('event_analysis_details')
    op.drop_table('column_master')
    op.drop_table('event_master')
    op.drop_table('module_master')
    # ### end Alembic commands ###