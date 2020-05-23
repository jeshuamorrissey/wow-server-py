# type: ignore[operator]

import argparse
import gzip
import json
import logging
import os
from typing import Any, Dict, List, Set, Text, Type

import coloredlogs
from construct import (Adapter, Array, Bytes, Computed, Const, Float32l,
                       Int32ul, Int64ul, Struct)
from mpyq import MPQArchive

from database import constants, db
from database.constants import common


class StringRefAdapater(Adapter):
    """Adapter which will map the given string index to the actual string."""

    def _decode(self, obj, context, path):
        if 'strings' in context['_']:
            strings = context['_'].strings
        elif 'strings' in context['_']['_']:
            strings = context['_']['_'].strings
        return strings.get(obj, '')

    def _encode(self, obj, context, path):
        for idx, string in context['_'].strings:
            if string == obj:
                return idx

        return 0


StringRef = StringRefAdapater(Int32ul)
LangStringRef = Struct(
    'en_us' / StringRef,
    'ko_kr' / StringRef,
    'fr_fr' / StringRef,
    'de_de' / StringRef,
    'en_cn' / StringRef,
    'en_tw' / StringRef,
    'es_es' / StringRef,
    'es_mx' / StringRef,
    'flags' / Int32ul,
)


def generate_struct(cls: Type) -> Struct:
    """Generate the construct.Struct object for a given entity class.

    Args:
        cls: The entity class to generate a struct from.

    Returns:
        A struct which can be used to load records matching the database type.
    """
    struct_fields = []
    for attr in cls._attrs_:
        if attr.name.endswith('_backlink'):
            continue

        if attr.py_type == int:
            struct_fields.append(attr.name / Int32ul)
        elif attr.py_type in (common.SingleString, common.SingleEnumString):
            struct_fields.append(attr.name / StringRef)
        elif attr.py_type in (common.MultiString, common.MultiEnumString,
                              common.MultiEnumSecondaryString):
            struct_fields.append(attr.name / LangStringRef)
        elif attr.py_type == float:
            struct_fields.append(attr.name / Float32l)
        else:
            if attr.py_type == cls.__name__:
                struct_fields.append((attr.name + '_fk') / Int32ul)
            else:
                struct_fields.append(attr.name / Int32ul)

    return Struct(*struct_fields)


def _load_string_block(c):
    """Load a string block from the construct.Struct context."""
    strings = {}
    index = 0
    for string in [s.decode('utf-8') for s in c.string_block.split(b'\x00')]:
        strings[index] = string
        index += len(string) + 1

    return strings


DBCFile = Struct(
    'header' / Struct(
        Const(b'WDBC'),
        'record_count' / Int32ul,
        'field_count' / Int32ul,
        'record_size' / Int32ul,
        'string_block_size' / Int32ul,
    ),
    'records' / Array(
        lambda c: c.header.record_count,
        Bytes(lambda c: c.header.record_size),
    ),
    'string_block' / Bytes(lambda c: c.header.string_block_size),
    'strings' / Computed(_load_string_block),
)


class MPQMultiArchive:
    """Wrapper around MPQArchive which allows patching multiple archives.

    This will load each archive in sequence and, when retreiving files, return the value
    from the latest archive first.
    """

    def __init__(self, base_path: Text, *archives: Text):
        """Create a new multi-archive.

        Args:
            base_path: The path to the WoW client.
            *archives: A list of MPQ archive names to load from the client.
        """
        self.archives = [
            MPQArchive(os.path.join(base_path, 'Data', a)) for a in archives
        ]

    @property
    def files(self) -> Set[Text]:
        """Get a list of files over all archives."""
        files = set()
        for a in self.archives:
            files.update([f for f in a.files if f.endswith(b'dbc')])

        return files

    def read_file(self, fname: Text) -> bytes:
        """Get a single file out from the archives.
        
        Raises:
            KeyError: raised if the file could not be found in any archives.
        """
        for a in self.archives[::-1]:
            contents = a.read_file(fname)
            if contents:
                return contents

        raise KeyError(f'Unknown file {fname}')


def num_fields_in_struct(struct: Struct) -> int:
    """Calculate the number of fields within a construct.Struct struct.

    This is a little tricky because we could have recursive structs.

    Args:
        struct: The struct definition.

    Returns:
        The number of concrete fields in the struct.
    """
    n = len(struct.subcons or struct.count)
    for subcon in struct.subcons:
        if hasattr(subcon, 'subcons'):
            n += num_fields_in_struct(subcon) - 1
    return n


def struct_to_dict(record: Struct) -> Dict[Text, Any]:
    """Convert the given loaded struct into a simple dictionary.

    Args:
        record: A loaded struct instance.
    
    Returns:
        A dictionary version of the struct (which can be put into the database).
    """
    d = {k: v for k, v in record.items() if not k.startswith('_')}
    for k, v in d.items():
        if hasattr(v, 'items'):
            # For LangStringRef's, just keep the en_us version.
            if 'en_us' in d[k]:
                d[k] = d[k]['en_us']
            else:
                d[k] = struct_to_dict(v)
    return d


def main(wow_dir: Text, output_dir: Text):
    coloredlogs.install()

    dbc_classes = {c.__name__: c for c in db.db.Entity.__subclasses__()}

    multi_archive = MPQMultiArchive(wow_dir, 'dbc.MPQ', 'patch.MPQ',
                                    'patch-2.MPQ')
    for fname in sorted(multi_archive.files):
        record_name = fname.decode('utf-8').split('\\')[1].split('.')[0]
        cls = dbc_classes.get(record_name, None)
        if not cls:
            logging.debug(f'Warning: no record format found for {record_name}!')
            continue

        # Make a struct from this class.
        logging.info(f'Loading {record_name}... ')
        dbc_file = DBCFile.parse(multi_archive.read_file(fname))
        record_struct = generate_struct(cls)

        if record_struct.sizeof(
        ) != dbc_file.header.record_size or num_fields_in_struct(
                record_struct) != dbc_file.header.field_count:
            logging.info(
                f'{record_name} is not a valid size (size is "{record_struct.sizeof()}", should be "{dbc_file.header.record_size}") (field count is "{num_fields_in_struct(record_struct)}", should be "{dbc_file.header.field_count}")!'
            )
            continue

        records = []
        for record_data in dbc_file.records:
            record = record_struct.parse(record_data, strings=dbc_file.strings)

            # HACK: APPLY TRANSFORMATIONS TO OBVIOUSLY WRONG DBC ENTRIES
            # For some reason, Gnomes and Troll have the wrong faction ID.
            if cls == constants.ChrRaces:
                if record['id'] == 7:
                    record['faction'] = 54
                elif record['id'] == 8:
                    record['faction'] = 530
                elif record['id'] == 9:
                    record['cinematic_sequence'] = None

            # Foreign keys use 0 but should use None.
            if cls == constants.CinematicSequences:
                for i in range(1, 8 + 1):
                    if getattr(record, f'camera{i}') == 0:
                        delattr(record, f'camera{i}')

            if cls == constants.ItemSubClass:
                if record['class_'] == 4294967295:
                    continue
                if record['sub_class'] == 4294967295:
                    continue
            # END HACK

            records.append(struct_to_dict(record))

        output = json.dumps(records)
        with gzip.GzipFile(filename=os.path.join(output_dir,
                                                 f'{record_name}.json.gz'),
                           mode='wb') as f:
            f.write(output.encode('ascii'))

        # with open(os.path.join(output_dir, f'{record_name}.json'), 'wb') as f:
        #     f.write(output.encode('ascii'))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--wow_dir',
        type=str,
        required=True,
        help='The absolute path to the World of Warcraft directory.')
    arg_parser.add_argument(
        '--output_dir',
        type=str,
        required=True,
        help='The absolute path to the output JSON file directory.')

    args = arg_parser.parse_args()
    main(args.wow_dir, args.output_dir)
