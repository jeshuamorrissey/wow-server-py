import os
import shutil
import tempfile

import pytest
from pony import orm

from database import data, db

_db_tempfile = tempfile.NamedTemporaryFile()


def pytest_configure(config):
    _db_tempfile.close()
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
