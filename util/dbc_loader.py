# type: ignore[operator]

import os
import argparse
import gzip
from typing import List, Text, Set
from mpyq import MPQArchive
from database.dbc.dbc import *
import json
from construct import Struct, Const, Int32ul, Array, Bytes, Computed, Adapter, Float32l, Int64ul


class StringRefAdapater(Adapter):

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


def GenerateStruct(cls) -> Struct:
    struct_fields = []
    for attr in cls._attrs_:
        if attr.name.endswith('_backlink'):
            continue

        if attr.py_type == int:
            struct_fields.append(attr.name / Int32ul)
        elif attr.py_type in (SingleString, SingleEnumString):
            struct_fields.append(attr.name / StringRef)
        elif attr.py_type in (MultiString, MultiEnumString, MultiEnumSecondaryString):
            struct_fields.append(attr.name / LangStringRef)
        elif attr.py_type == float:
            struct_fields.append(attr.name / Float32l)
        elif attr.py_type == FixedIntArray:
            struct_fields.append(attr.name / Array(attr.size, Int32ul))
        else:
            if attr.py_type == cls.__name__:
                struct_fields.append((attr.name + '_fk') / Int32ul)
            else:
                struct_fields.append(attr.name / Int32ul)

    return Struct(*struct_fields)


def LoadStringBlock(c):
    strings = {}
    index = 0
    for string in [s.decode('utf-8') for s in c.string_block.split(b'\x00')]:
        strings[index] = string
        index += len(string) + 1

    return strings


def NumFieldsInStruct(struct: Struct):
    n = len(struct.subcons or struct.count)
    for subcon in struct.subcons:
        if hasattr(subcon, 'subcons'):
            n -= 1
            n += NumFieldsInStruct(subcon)
    return n


def StructToDict(record):
    d = {k: v for k, v in record.items() if not k.startswith('_')}
    for k, v in d.items():
        if hasattr(v, 'items'):
            if 'en_us' in d[k]:
                d[k] = d[k]['en_us']
            else:
                d[k] = StructToDict(v)
    return d


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
    'strings' / Computed(LoadStringBlock),
)


class MPQMultiArchive:

    def __init__(self, base_path: Text, *archives: Text):
        self.archives = [MPQArchive(os.path.join(base_path, 'Data', a)) for a in archives]

    @property
    def files(self) -> Set[Text]:
        files = set()
        for a in self.archives:
            files.update([f for f in a.files if f.endswith(b'dbc')])

        return files

    def read_file(self, fname: Text) -> bytes:
        for a in self.archives[::-1]:
            contents = a.read_file(fname)
            if contents:
                return contents

        raise RuntimeError(f'Unknown file {fname}')


def main(wow_dir: Text, output_dir: Text):
    multi_archive = MPQMultiArchive(wow_dir, 'dbc.MPQ', 'patch.MPQ', 'patch-2.MPQ')
    for fname in multi_archive.files:
        record_name = fname.decode('utf-8').split('\\')[1].split('.')[0]
        cls = globals().get(record_name, None)
        if not cls:
            # print(f'Warning: no record format found for {record_name}!')
            continue

        # Make a struct from this class.
        print(f'Loading {record_name}... ')
        dbc_file = DBCFile.parse(multi_archive.read_file(fname))
        record_struct = GenerateStruct(cls)

        if record_struct.sizeof() != dbc_file.header.record_size or NumFieldsInStruct(
                record_struct) != dbc_file.header.field_count:
            print(
                f'{record_name} is not a valid size (size is "{record_struct.sizeof()}", should be "{dbc_file.header.record_size}") (field count is "{NumFieldsInStruct(record_struct)}", should be "{dbc_file.header.field_count}")!'
            )
            continue

        records = []
        for record_data in dbc_file.records:
            record = record_struct.parse(record_data, strings=dbc_file.strings)

            # HACK: APPLY TRANSFORMATIONS TO OBVIOUSLY WRONG DBC ENTRIES
            # For some reason, Gnomes and Troll have the wrong faction ID.
            if cls == ChrRaces:
                if record['id'] == 7:
                    record['faction'] = 54
                elif record['id'] == 8:
                    record['faction'] = 530
                elif record['id'] == 9:
                    record['cinematic_sequence'] = None

            # Foreign keys use 0 == None.
            if cls == CinematicSequences:
                for i in range(1, 8 + 1):
                    if getattr(record, f'camera{i}') == 0:
                        delattr(record, f'camera{i}')
            # END HACK

            records.append(StructToDict(record))

        output = json.dumps(records)
        with gzip.GzipFile(filename=os.path.join(output_dir, f'{record_name}.json.gz'), mode='wb') as f:
            f.write(output.encode('ascii'))

        with open(os.path.join(output_dir, f'{record_name}.json'), 'wb') as f:
            f.write(output.encode('ascii'))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--wow_dir',
                            type=str,
                            required=True,
                            help='The absolute path to the World of Warcraft directory.')
    arg_parser.add_argument('--output_dir',
                            type=str,
                            required=True,
                            help='The absolute path to the output JSON file directory.')

    args = arg_parser.parse_args()
    main(args.wow_dir, args.output_dir)
