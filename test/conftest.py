import enum

import pytest
from pony import orm

from database import common, constants, game, world
from database.db import db


def pytest_configure(config):
    db.bind(provider='sqlite', filename='memory', create_db=True)
    db.provider.converter_classes.append((enum.Enum, common.EnumConverter))
    db.generate_mapping(create_tables=True)


def pytest_runtest_setup(item):
    orm.db_session.__enter__()


def pytest_runtest_teardown(item, nextitem):
    orm.db_session.__exit__()

    db.drop_all_tables(with_all_data=True)
    db.create_tables()


@pytest.fixture
def fake_db():
    yield db
