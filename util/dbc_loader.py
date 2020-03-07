# type: ignore[operator]

import os
import argparse
import gzip
from mpyq import MPQArchive
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

AnimationData = Struct(
    'id' / Int32ul,
    'name' / StringRef,
    'weapon_flags' / Int32ul,
    'body_flags' / Int32ul,
    'flags' / Int32ul,
    'fallback' / Int32ul,
    'previous' / Int32ul,
)

AreaPOI = Struct(
    'id' / Int32ul,
    'importance' / Int32ul,
    'icon' / Int32ul,
    'faction_id' / Int32ul,
    'x' / Float32l,
    'y' / Float32l,
    'z' / Float32l,
    'continent_id' / Int32ul,
    'flags' / Int32ul,
    Int32ul,  # unk
    'name' / LangStringRef,
)

AreaTrigger = Struct(
    'id' / Int32ul,
    'continent_id' / Int32ul,
    'x' / Float32l,
    'y' / Float32l,
    'z' / Float32l,
    'radius' / Float32l,
    'box_length' / Float32l,
    'box_width' / Float32l,
    'box_height' / Float32l,
    'box_yaw' / Float32l,
)


def LoadStringBlock(c):
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
    'strings' / Computed(LoadStringBlock),
)


def NumFieldsInStruct(struct: Struct):
    n = len(struct.subcons)
    for subcon in struct.subcons:
        if hasattr(subcon, 'subcons'):
            n -= 1
            n += NumFieldsInStruct(subcon)
    return n


def StructToDict(record):
    d = {k: v for k, v in record.items() if not k.startswith('_')}
    for k, v in d.items():
        if hasattr(v, 'items'):
            d[k] = StructToDict(v)
    return d


def main(wow_dir: str, output_dir: str):
    archive = MPQArchive(os.path.join(wow_dir, 'Data', 'dbc.MPQ'))
    for fname in archive.files:
        record_name = fname.decode('utf-8').split('\\')[1].split('.')[0]
        dbc_file = DBCFile.parse(archive.read_file(fname))
        cls: Struct = globals().get(record_name, None)
        if not cls:
            # print(f'Warning: no record format found for {record_name}!')
            continue

        if cls.sizeof() != dbc_file.header.record_size or NumFieldsInStruct(cls) != dbc_file.header.field_count:
            print(
                f'{record_name} is not a valid size (size is "{cls.sizeof()}", should be "{dbc_file.header.record_size}") (field count is "{NumFieldsInStruct(cls)}", should be "{dbc_file.header.field_count}")!'
            )
            continue

        records = []
        for record_data in dbc_file.records:
            record = cls.parse(record_data, strings=dbc_file.strings)
            records.append(StructToDict(record))

        output = json.dumps(records)
        with gzip.GzipFile(filename=os.path.join(output_dir, f'{record_name}.json.gz'), mode='wb') as f:
            print(f'Writing {record_name}...')
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
