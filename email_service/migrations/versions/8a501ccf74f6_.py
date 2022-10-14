"""empty message

Revision ID: 8a501ccf74f6
Revises: af04514faac6
Create Date: 2022-10-14 22:41:29.353133

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8a501ccf74f6'
down_revision = 'af04514faac6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sent_to', sa.String(length=120), nullable=False),
    sa.Column('date_sent', sa.DateTime(), nullable=False),
    sa.Column('email_opened', sa.Boolean(), nullable=True),
    sa.Column('email_clicked', sa.Boolean(), nullable=True),
    sa.Column('postmark_message_id', sa.String(), nullable=True),
    sa.Column('email_template_version', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['email_template_version'], ['pm_template_version.postmark_template_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('transactions')
    op.create_unique_constraint(None, 'pm_templates', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pm_templates', type_='unique')
    op.create_table('transactions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sent_to', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('date_sent', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('email_opened', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('email_clicked', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('postmark_message_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email_template_version', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['email_template_version'], ['pm_template_version.postmark_template_id'], name='transactions_email_template_version_fkey'),
    sa.PrimaryKeyConstraint('id', name='transactions_pkey')
    )
    op.drop_table('email_transactions')
    # ### end Alembic commands ###