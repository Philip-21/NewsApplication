"""add foreign-key to newspost table

Revision ID: 0632b9098226
Revises: 59640ebc9b1e
Create Date: 2022-03-08 21:12:33.709406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0632b9098226'
down_revision = '59640ebc9b1e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("newspost",
    sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key("newspost_users_fk", source_table="newspost", referent_table="users", local_cols=['owner_id'], remote_cols=["id"],ondelete='CASCADE')
    #foreign connects columns btwn tables for them to have a relationship the owner id in newspost table will generate the same id in the users table i.e the users table is the reference table
    pass


def downgrade():
    op.drop_constrain("newspost_users_fk", table_name="newspost")
    op.drop_column("newspost", "owner_id")
    pass
