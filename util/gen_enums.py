import argparse
import logging
import re
import string
from typing import Text

import coloredlogs
import stringcase
from pony import orm

from database import db
from database.constants import common


def main(output_file: Text):
    coloredlogs.install(level=logging.DEBUG)
    db.SetupDatabase(db_file=':memory:')

    logging.debug('Generating enums...')
    lines = ['import enum', '']
    enum_lines = {}
    for cls in db.db.Entity.__subclasses__():
        enum_name = None
        enum_field = None
        secondary_enum_field = None

        for attr in cls._attrs_:
            if attr.py_type in (common.SingleEnumString, common.MultiEnumString):
                enum_name = 'E' + cls.__name__
                enum_field = attr.name
            elif attr.py_type in (common.MultiEnumSecondaryString,):
                secondary_enum_field = attr.name

        if not enum_name or not enum_field:
            continue

        if secondary_enum_field:
            logging.info(f'Processing {cls.__name__} (enum fields "{enum_field}", "{secondary_enum_field}")')
        else:
            logging.info(f'Processing {cls.__name__} (enum field "{enum_field}")')

        SPECIAL_CHARS = string.punctuation.replace('%', '').replace('_', '')

        enums = {}
        with orm.db_session:
            for r in cls.select():
                name = ''.join(c for c in getattr(r, enum_field) if c not in SPECIAL_CHARS)
                name = name.replace('%', '_percent')
                if secondary_enum_field and getattr(r, secondary_enum_field):
                    name += '_' + getattr(r, secondary_enum_field)
                name = stringcase.constcase(name)
                if name[0].isnumeric():
                    name = '_' + name
                name = re.sub('_+', '_', name)
                if cls.__name__ == 'ItemSubClass':
                    enums[name] = r.sub_class
                else:
                    enums[name] = r.id

        enum_lines[enum_name] = [f'class {enum_name}(enum.IntEnum):']
        for k, v in sorted(enums.items()):
            enum_lines[enum_name].append(f'    {k} = {v}')
        enum_lines[enum_name].append('')

    for _, el in sorted(enum_lines.items()):
        lines.extend(el)

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
