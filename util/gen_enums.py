import argparse
import logging
import re
from typing import Text

import coloredlogs
import stringcase
from pony import orm

from database import db
from database.dbc import dbc


def main(output_file: Text):
    coloredlogs.install(level=logging.DEBUG)
    db.SetupDatabase(db_file=':memory:')

    lines = ['import enum', '']
    for cls in db.db.Entity.__subclasses__():
        enum_name = None
        enum_field = None

        for attr in cls._attrs_:
            if attr.py_type in (dbc.SingleEnumString, dbc.MultiEnumString):
                enum_name = cls.__name__
                enum_field = attr.name
                break

        if not enum_name or not enum_field:
            continue

        with orm.db_session:
            lines.append(f'class {enum_name}(enum.IntEnum):')
            for id, name in orm.select((r.id, getattr(r, enum_field)) for r in cls).order_by(1):
                name = ''.join(c for c in name if c not in '\'",-(){}+/!:[]')
                name = stringcase.constcase(name)
                if name[0].isnumeric():
                    name = '_' + name
                name = re.sub('_+', '_', name)
                lines.append(f'    {name} = {id}')
            lines.append('')

    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--output_file',
                            type=str,
                            required=True,
                            help='The absolute path to the output JSON file directory.')

    args = arg_parser.parse_args()
    main(args.output_file)
