import gzip
import json
import logging
import os

from pony import orm

from database.db import db
from database.dbc.dbc import AnimationData, AreaPOI, AreaTrigger, AttackAnimKits, AttackAnimTypes, AuctionHouse, Faction, BankBagSlotPrices, ChrRaces, Languages, CreatureType, Spell, CinematicCamera, CinematicSequences
from database.dbc import (char_start_outfit, chr_start_locations, item_template, profession, quest_template,
                          spell_template, unit_template)

_LOAD_ORDER = [
    AnimationData,
    AreaPOI,
    AreaTrigger,
    AttackAnimTypes,
    AttackAnimKits,
    Faction,
    AuctionHouse,
    BankBagSlotPrices,
    Languages,
    CreatureType,
    CinematicCamera,
    CinematicSequences,
    Spell,
    ChrRaces,
    # char_start_outfit.CharStartOutfit,
    # chr_races.ChrRaces,
    # chr_start_locations.ChrStartLocation,
    # item_template.ItemTemplate,
    # profession.Profession,
    # quest_template.QuestTemplate,
    # quest_template.Objective,
    # spell_template.SpellTemplate,
    # unit_template.UnitTemplate,
]


@orm.db_session
def LoadDBC():
    for cls in _LOAD_ORDER:
        base_file = f'database/dbc/data/{cls.__name__}'
        data_file = None
        if os.path.exists(f'{base_file}.json.gz'):
            data_file = f'{base_file}.json.gz'
        elif os.path.exists(f'{base_file}.json'):
            data_file = f'{base_file}.json'

        if data_file:
            with orm.db_session:
                if orm.count(r for r in cls) == 0:
                    logging.info(f'Loading {cls.__name__}...')

                    if data_file.endswith('.gz'):
                        f = gzip.GzipFile(data_file)
                    else:
                        f = open(data_file)

                    # We have to load the static data in 2 phases:
                    #
                    #     1. The first phase will load all of the non-foreign-key values.
                    #     2. The second phase will load all foreign-key values.
                    #
                    # This is because some tables have self referential foreign keys, which means
                    # we have to create all entries in the table first otherwise we will get
                    # foreign key errors. PonyORM should be able to handle this for us, but unfortunately
                    # it tries to be "smart" and auto-create objects that don't already exist. This
                    # causes weird exceptions.
                    #
                    # These self-foreign-keys are identified with a '_fk' suffix.
                    records = json.load(f)

                    keys = [k for k in records[0].keys() if not k.endswith('_fk')]
                    fk_keys = [k for k in records[0].keys() if k.endswith('_fk')]

                    # Load the non-FK components.
                    for r in records:
                        cls(**{k: r.get(k, None) for k in keys})

                    # Load the FK components.
                    if fk_keys:
                        for r in records:
                            obj = cls.get(**{k: r[k] for k in keys})
                            for k in fk_keys:
                                try:
                                    cls[r[k]]
                                    setattr(obj, k[:-3], r[k])
                                except orm.ObjectNotFound:
                                    setattr(obj, k[:-3], None)

                                orm.flush()  # flush here to force a save and to avoid save chains
