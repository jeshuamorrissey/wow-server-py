import gzip
import json
import logging
import os

from pony import orm

from database.db import db
from database.dbc import (char_start_outfit, chr_races, chr_start_locations, item_template, profession, quest_template,
                          spell_template, unit_template)

_LOAD_ORDER = [
    char_start_outfit.CharStartOutfit,
    chr_races.ChrRaces,
    chr_start_locations.ChrStartLocation,
    item_template.ItemTemplate,
    profession.Profession,
    quest_template.QuestTemplate,
    quest_template.Objective,
    spell_template.SpellTemplate,
    unit_template.UnitTemplate,
]


@orm.db_session
def LoadDBC():
    for cls in _LOAD_ORDER:
        base_file = f'database/dbc/data/{cls.__name__}'
        data_file = None
        if os.path.exists(f'{base_file}.json'):
            data_file = f'{base_file}.json'
        elif os.path.exists(f'{base_file}.json.gz'):
            data_file = f'{base_file}.json.gz'

        if data_file:
            if orm.count(r for r in cls) == 0:
                logging.info(f'Loading {cls.__name__}...')

                if data_file.endswith('.gz'):
                    f = gzip.GzipFile(data_file)
                else:
                    f = open(data_file)

                for r in json.load(f):
                    cls(**r)
