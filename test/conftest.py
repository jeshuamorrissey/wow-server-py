import enum

import pytest
from pony import orm

from database import common, constants, data, game, world
from database.db import db


def pytest_configure(config):
    db.bind(provider='sqlite', filename='/tmp/test.db', create_db=True)
    db.provider.converter_classes.append((enum.Enum, common.EnumConverter))
    db.generate_mapping(create_tables=True)

    print('Loading base data, this will take some time the first time...')
    data.load_constants(db)
    print('Done!')


def pytest_runtest_setup(item):
    data.clear_world_database(db)
    db.create_tables()
    orm.db_session.__enter__()


def pytest_runtest_teardown(item, nextitem):
    orm.db_session.__exit__()


@pytest.fixture
def fake_db():
    yield db
