import enum
import logging
import os
import shutil
import socket
import tempfile
import threading

import pytest
from pony import orm

from common import server
from database import common, constants, data, db, game, world

_db_tempfile = tempfile.NamedTemporaryFile()


def pytest_configure(config):
    shutil.copy(os.path.join(os.getcwd(), 'test/base.db'), _db_tempfile.name)
    db.SetupDatabase(db_file=_db_tempfile.name)


def pytest_runtest_setup(item):
    data.clear_world_database(db.db)
    db.db.create_tables()
    orm.db_session.__enter__()


def pytest_runtest_teardown(item, nextitem):
    orm.flush()
    orm.db_session.__exit__()


@pytest.fixture
def fake_db():
    yield db.db
