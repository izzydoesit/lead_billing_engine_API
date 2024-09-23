"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def check_version(connection):
    # Example check, customize as needed
    result = connection.execute(text("SELECT version_num FROM alembic_version")).fetchone()
    if result:
        current_version = result[0]
        logger.info(f"Current DB version: {current_version}")
        if current_version != "${down_revision}":
            raise Exception(f"Expected version ${down_revision} but found {current_version}")
    else:
        logger.info("No version found in alembic_version table.")

def upgrade():
    connection = op.get_bind()
    logger.info("Applying upgrade to ${up_revision}")
    try:
        check_version(connection)
        ${'\n'.join('    ' + line for line in (upgrades or "pass").split('\n'))}
        logger.info("Successfully applied upgrade to ${up_revision}")
    except Exception as e:
        logger.error(f"Failed to apply upgrade to ${up_revision}: {e}")
        raise e

def downgrade():
    connection = op.get_bind()
    logger.info("Reverting upgrade to ${up_revision}")
    try:
        ${'\n'.join('    ' + line for line in (downgrades or "pass").split('\n'))}
        logger.info("Successfully reverted upgrade to ${up_revision}")
    except Exception as e:
        logger.error(f"Failed to revert upgrade to ${up_revision}: {e}")
        raise e
