"""create newspost table

Revision ID: a2746ccebea1
Revises: 
Create Date: 2022-03-08 20:38:33.066731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2746ccebea1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("newspost",
    sa.Column("id",sa.Integer(),nullable=False),
    sa.Column("title",sa.String(),nullable=False),
    sa.Column("content",sa.String(),nullable=False),
    sa.Column("comments",sa.String(),nullable=False),
    sa.Column("published",sa.Boolean(),default=True),
    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")),
    sa.PrimaryKeyConstraint("id")
    )
    pass


def downgrade():
    op.drop_table("newspost")
    pass
