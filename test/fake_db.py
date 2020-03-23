import enum
import unittest

from database import common, constants, game, world
from database.db import db


class TestWithDatabase(unittest.TestCase):

    @staticmethod
    def setUpClass():
        db.bind(provider='sqlite', filename=':memory:', create_db=True)
        db.provider.converter_classes.append((enum.Enum, common.EnumConverter))
        db.generate_mapping(create_tables=True)

    def setUp(self):
        super(TestWithDatabase, self).setUp()
        db.drop_all_tables(with_all_data=True)
        db.create_tables()
