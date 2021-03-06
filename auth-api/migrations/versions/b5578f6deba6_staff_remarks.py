"""staff remarks

Revision ID: b5578f6deba6
Revises: 7f01a013a976
Create Date: 2021-06-10 23:00:12.600023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5578f6deba6'
down_revision = '7f01a013a976'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    staff_remark_codes = op.create_table('staff_remark_codes',
    sa.Column('code', sa.String(length=15), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )

    op.bulk_insert(
        staff_remark_codes,
        [
            {
                "code": "BLANKAFFIDAVIT",
                "description": "Affidavit is blank / affidavit is not attached",
                "default": False
            },
            {
                "code": "MISSINGSEAL",
                "description": "Affidavit is missing seal",
                "default": False
            },
            {
                "code": "INCOMPLETE",
                "description": "One or more required fields is incomplete",
                "default": False
            },
            {
                "code": "NOTPRACTICING",
                "description": "Lawyer/notary is not practicing",
                "default": False
            },
            {
                "code": "NAMEMISMATCH",
                "description": "User profile name does not match the name on the affidavit",
                "default": False
            },
        ]
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('staff_remark_codes')
    # ### end Alembic commands ###
