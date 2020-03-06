import gzip
import json
import logging
import os

from pony import orm

from database.db import db
from database.dbc import *


@orm.db_session
def LoadDBC():
    for cls in db.Entity.__subclasses__():
        data_file = None
        if os.path.exists(f'database/dbc/data/{cls.__name__}.json'):
            data_file = f'database/dbc/data/{cls.__name__}.json'
        elif os.path.exists(f'database/dbc/data/{cls.__name__}.json.gz'):
            data_file = f'database/dbc/data/{cls.__name__}.json.gz'

        if data_file:
            if orm.count(r for r in cls) == 0:
                logging.info(f'Loading {cls.__name__}...')

                if data_file.endswith('.gz'):
                    f = gzip.GzipFile(data_file)
                else:
                    f = open(data_file)

                for r in json.load(f):
                    cls(**r)
