import gzip
import json
import logging
import os
from typing import Set, Text, Type, Dict

from pony import orm

from database.db import db

_LOADED: Set[Text] = set()


def _Load(cls_name: Text, cls: Type, all_cls: Dict[Text, Type], dependencies: Dict[Text, Set[Text]]):
    """Load the given class' data file.

    Args:
        cls_name: The name of the class to load.
        cls: The type of the class to load.
        all_cls: A mapping of class names --> types (all of them).
        dependencies: A mapping of class names --> dependent class names.
    """
    if cls_name in _LOADED:
        return

    _LOADED.add(cls_name)

    for dep in dependencies.get(cls_name, set()):
        _Load(dep, all_cls[dep], all_cls, dependencies)

    base_file = f'database/dbc/data/{cls_name}'
    data_file = None
    if os.path.exists(f'{base_file}.json.gz'):
        data_file = f'{base_file}.json.gz'
    elif os.path.exists(f'{base_file}.json'):
        data_file = f'{base_file}.json'
    else:
        return

    with orm.db_session:
        if orm.count(r for r in cls) == 0:
            logging.info(f'Loading {cls_name}...')

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


def _FindSubclasses(cls: Type) -> Dict[Text, Type]:
    subclasses = {}
    for subclass in cls.__subclasses__():
        subclasses[subclass.__name__] = subclass
        subclasses.update(_FindSubclasses(subclass))

    return subclasses


@orm.db_session
def LoadDBC():
    entity_types = _FindSubclasses(db.Entity)
    dependencies = {entity_name: set() for entity_name in entity_types}
    for entity_name, entity_type in entity_types.items():
        for attr in entity_type._attrs_:
            if issubclass(attr.py_type,
                          db.Entity) and attr.py_type.__name__ != entity_name and not attr.name.endswith('_backlink'):
                dependencies[entity_name].add(attr.py_type.__name__)

    for entity_name, entity_type in sorted(entity_types.items()):
        _Load(entity_name, entity_type, entity_types, dependencies)