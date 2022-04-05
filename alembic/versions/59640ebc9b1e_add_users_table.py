"""add users table

Revision ID: 59640ebc9b1e
Revises: a2746ccebea1
Create Date: 2022-03-08 20:59:13.937627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59640ebc9b1e'
down_revision = 'a2746ccebea1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
    sa.Column("id",sa.Integer,nullable=False),
    sa.Column("email",sa.String, nullable=False),
    sa.Column("password",sa.String, nullable=False),
    sa.Column( "created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")),#time post is created 
    sa.PrimaryKeyConstraint("id"),#the id column makes each entry in a row unique ,
    sa.UniqueConstraint('email'))#unique prevents duplicate emails 
    pass
    

def downgrade():
    op.drop_table("users")
    pass
