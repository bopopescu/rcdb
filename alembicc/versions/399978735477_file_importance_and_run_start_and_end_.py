"""File importance and run start and end times

Revision ID: 399978735477
Revises: 5394f8fc7257
Create Date: 2017-04-20 18:37:38.982675

"""

# revision identifiers, used by Alembic.
revision = '399978735477'
down_revision = '5394f8fc7257'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('importance', sa.Integer(), server_default='0', nullable=False))
    # ### end Alembic commands ###
    
    from alembic import context
    from datetime import datetime
    from rcdb.provider import RCDBProvider
    from rcdb.model import ConditionType

    x_args = context.get_x_argument(as_dictionary=True)

    # It is very important, if we run it programmatically
    # we have rcdb_connection. Otherwise connection_string is taken from alembic.ini
    # (!) don't be confused by replacement of alembic_config["sqlalchemy.url"] in env.py
    # in this file it reads the value from alembic.ini
    if "rcdb_connection" in x_args:
        connection_string = x_args["rcdb_connection"]
    else:
        alembic_config = context.config.get_section(context.config.config_ini_section)
        connection_string = alembic_config["sqlalchemy.url"]

    # Create RCDBProvider object that connects to DB and provide most of the functions
    db = RCDBProvider(connection_string, check_version=False)

    # Create condition type
    db.create_condition_type("run_start_time", ConditionType.TIME_FIELD, "Run start time")
    db.create_condition_type("run_end_time", ConditionType.TIME_FIELD, "Run end (or last record) time")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('files', 'importance')
    # ### end Alembic commands ###