import gzip
import json
import logging
import os
import time
from typing import IO, Dict, List, Optional, Set, Text, Type, Union

from pony import orm


def _load(db: orm.Database, cls_name: Text, cls: Type, module: Text):
    """Load the given class' data file.

    Args:
        db: The database we are loading into.
        cls_name: The name of the class to load.
        cls: The type of the class to load.
        module: The module the class is in (either "constants" or "game")
    """
    base_file = f'database/{module}/data/{cls_name}'
    data_file = None
    if os.path.exists(f'{base_file}.json.gz'):
        data_file = f'{base_file}.json.gz'
    elif os.path.exists(f'{base_file}.json'):
        data_file = f'{base_file}.json'
    else:
        return

    with orm.db_session:
        if orm.count(r for r in cls) == 0:
            logging.info(f'Loading {cls_name} from {data_file}...')

            f: Optional[Union[IO, gzip.GzipFile]] = None
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
                for attr in cls._attrs_:
                    if issubclass(attr.py_type, db.Entity) and r.get(attr.name, None) == '0':
                        del r[attr.name]

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

                        # Flush here to force a save and to avoid save chains.
                        orm.flush()


def _sorted_by_dependencies(classes: Dict[Text, Type]) -> List[Set[Text]]:
    """Return a sorted list of classes based on dependency order.

    This will resolve dependencies by inspecting the class attributes and determine
    the required order for class loading.

    Args:
        classes: A mapping from class name --> class type.
    
    Returns:
        A list of sets. Each set is a "phase"; anything within a phase can be loaded at
        the same time, but phases must be sequential.
    """
    # First, build up a simple dependency graph.
    dependencies: Dict[Text, Set[Text]] = {entity_name: set() for entity_name in classes}
    for entity_name, entity_type in classes.items():
        for attr in entity_type._attrs_:
            attr_type_name = attr.py_type.__name__

            # Special case: ignore self-links (assume they will be resolvable).
            if attr_type_name == entity_name:
                continue

            # Special case: ignore attributes which aren't the right type.
            if attr_type_name not in classes:
                continue

            # Special case: ignore backlinks.
            if attr.name.endswith('_backlink'):
                continue

            dependencies[entity_name].add(attr_type_name)

    # Now, do a topological sort.
    processed: Set[Text] = set()
    last_phase: Set[Text] = set()
    sorted_dependencies: List[Set[Text]] = []
    while True:
        phase: Set[Text] = set()

        # Find everything with no dependencies; these are in the next phase.
        for name, deps in dependencies.items():
            if name not in processed and len(deps - processed) == 0:
                phase.add(name)

        # If we got the same phase again, then we have reached a cycle :(
        if phase == last_phase:
            raise RuntimeError('Dependency graph produced a cycle! Are backlinks named correctly?')

        # If there was nothing in this phase, we must be done.
        if not phase:
            break

        sorted_dependencies.append(phase)
        processed.update(phase)
        last_phase = phase

    assert len(processed) == len(classes)
    return sorted_dependencies


def _find_subclasses(cls: Type, include_prefix=None) -> Dict[Text, Type]:
    """Find all subclasses of the given type (recusively).

    Args:
        cls: The object type to find subclasses of.
        include_prefix: A tuple of module prefixes to include.

    Returns:
        A mapping of subclass name --> subclass type.
    """
    if not include_prefix:
        include_prefix = ()

    subclasses = {}
    for subclass in cls.__subclasses__():
        # Ignore world classes; they have no static data.
        if not subclass.__module__.startswith(include_prefix):
            continue

        subclasses[subclass.__name__] = subclass
        subclasses.update(_find_subclasses(subclass))

    return subclasses


def clear_world_database(db: orm.Database):
    """Drop all of the world database tables and re-create them.

    This is useful to only clear the cheap to re-create test data and avoid having
    to reload the whole database each time.

    Args:
        db: The database to clear the tables from.
    """
    classes = _find_subclasses(db.Entity, include_prefix=('database.world',))

    for cls_name, cls in classes.items():
        logging.debug(f'Dropping table world.{cls_name}')
        cls.drop_table(with_all_data=True)


@orm.db_session
def load_constants(db: orm.Database):
    """Load the constant data files into the appropriate tables.

    Each of the database classes should have been imported by this point; this function
    uses db.Entity.__subclasses__() to discover classes we should populate data for.

    Args:
        db: The database to load the constants into.
    """
    classes = _find_subclasses(db.Entity, include_prefix=('database.constants', 'database.game'))
    load_order = _sorted_by_dependencies(classes)
    _profile: Dict[Text, float] = {}
    _longest_name_len = 0

    for i, phase in enumerate(load_order):
        logging.debug(f'Loading, phase {i}...')
        for entity_name in sorted(phase):
            module = classes[entity_name].__module__.split('.')[1]

            start_time = time.time()
            _load(db, entity_name, classes[entity_name], module)
            _profile[entity_name] = time.time() - start_time

    logging.debug('Profile information for database loading: ')
    _longest_name_len = max(len(name) for name in _profile.keys())
    for name, process_time in sorted(_profile.items(), key=lambda i: i[1], reverse=True):
        display_name = (' ' * (_longest_name_len - len(name))) + name
        logging.debug('{}: {:.4f}s'.format(display_name, process_time))
