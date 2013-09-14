"""Runs the database migration. It Checks to see if the db has been upgraded.
If so, it will invalidate the cache"""

import os
from alembic.script import ScriptDirectory
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic import command
from general import config
from app.database import engine
from app.lib import cache


def migrate():
    conf = Config(
        "%s/alembic.ini" % config.FLASK_BASE_PATH)
    script = ScriptDirectory.from_config(conf)
    head = script.get_current_head()

    context = MigrationContext.configure(engine.connect())
    current = context.get_current_revision()

    if head != current:
        # print "Will upgrade from %s to %s" % (current, head)
        command.upgrade(conf, "head")
        # print "Flushing cache"
        cache.flush_all()
    else:
        # print "Database up to date. No migrations run"


if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV')
    if not env:
        raise Exception('Error: Environment not set')
    # print "Starting Migration Script for: " + env
    migrate()
