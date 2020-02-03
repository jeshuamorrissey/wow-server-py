import enum
from construct import (Array, Bytes, Const, Enum, Float32l, GreedyBytes,
                       GreedyRange, If, Int8ul, Int32ul, Int64ul, Rebuild,
                       Struct, Switch, Adapter, Byte)

from database.dbc import constants as c

import struct


class PackedGUIDAdapter(Adapter):
    """Adapter which is capable of loading a packed GUID into an integer.

    It requires a struct with the following fields:
        - mask (a single byte mask)
        - parts (a list of GUID bytes)
    """
    def _decode(self, obj, context, path):
        guid_bytes = iter(obj.parts)

        guid = 0
        for i in range(8):
            if obj.mask & (1 << i):
                guid |= next(guid_bytes) << (i * 8)

        return guid

    def _encode(self, obj, context, path):
        mask = 0
        parts = []
        for i, byte in enumerate(obj.to_bytes(8, 'little')):
            if byte != 0:
                mask |= (1 << i)
                parts.append(byte)

        return dict(mask=mask, parts=parts)


PackedGUID = PackedGUIDAdapter(Struct(
    'mask' / Int8ul,
    'parts' / Array(lambda this: bin(this.mask).count('1'), Byte),
))

class UpdateFieldsAdapter(Adapter):
    """Adapter which can process the update fields in UPDATE_OBJECT.
    
    This will required an dictionary input of fields, and requires to be
    adapted around a struct with the following members:
        - blocks: the number of mask blocks
        - masks: a list of mask bytes
        - fields: a list of fields (each field is 4 bytes)

    When decoding, it will not preserve type information (there is no
    reasonable way to do this), but when encoding you can pass in either
    an int, float, bytes or enum.Enum.
    """
    def _decode(self, obj, context, path):
        result = {}

        fields = iter(obj.fields)
        mask = int.from_bytes(bytearray(obj.masks), 'little')
        for i in range(obj.blocks * 4):
            if mask & (1 << i):
                result[i] = next(fields)

        return result

    def _encode(self, obj, context, path):
        num_values = len(obj)

        # Calculate the number of mask blocks we need.
        blocks = (num_values + 32 - 1) // 32

        # Each mask block is 4 bytes long
        num_bytes = blocks * 4

        mask = 0
        fields = []
        for field, value in sorted(obj.items()):
            if value is None:
                continue

            mask |= (1 << field)
            if isinstance(value, int):
                if value < 0:
                    fields.append(value.to_bytes(4, 'little', signed=True))
                else:
                    fields.append(value.to_bytes(4, 'little'))
            elif isinstance(value, float):
                fields.append(struct.pack('f', value))
            elif isinstance(value, bytes):
                assert len(value) == 4
                fields.append(value)
            elif isinstance(value, enum.Enum):
                fields.append(value.value.to_bytes(4, 'little'))
            else:
                raise ValueError(f'unknown update field type {type(value)}')

        return dict(
            blocks=blocks,
            masks=list(mask.to_bytes(num_bytes, 'little')),
            fields=list(fields),
        )


UpdateFields = UpdateFieldsAdapter(Struct(
    'blocks' / Int8ul,
    'masks' / Array(lambda this: this.blocks * 4, Byte),
    'fields' / Array(lambda this: sum(bin(m).count('1')
                                      for m in this.masks), Bytes(4)),
))

is_set = lambda enum: lambda this: enum in this.flags
is_not_set = lambda enum: lambda this: enum not in this.flags

FullMovementUpdate = Struct(
    'flags' / Enum(Int32ul, c.MovementFlags),
    'time' / Int32ul,
    'x' / Float32l,
    'y' / Float32l,
    'z' / Float32l,
    'o' / Float32l,
    'transport' / If(
        is_set(c.MovementFlags.ONTRANSPORT),
        Struct(
            'guid' / Int64ul,
            'x' / Float32l,
            'y' / Float32l,
            'z' / Float32l,
            'o' / Float32l,
            'time' / Int32ul,
        )),
    'swimming' / If(
        is_set(c.MovementFlags.SWIMMING),
        Struct('pitch' / Float32l),
    ),
    'last_fall_time' / If(
        is_not_set(c.MovementFlags.ONTRANSPORT),
        Int32ul,
    ),
    'falling' / If(
        is_set(c.MovementFlags.FALLING),
        Struct(
            'velocity' / Float32l,
            'sin_angle' / Float32l,
            'cos_angle' / Float32l,
            'xy_speed' / Float32l,
        ),
    ),
    'spline_elevation' / If(
        is_set(c.MovementFlags.SPLINE_ELEVATION),
        Struct('unk1' / Float32l),
    ),
    'speed' / Struct(
        'walk' / Float32l,
        'run' / Float32l,
        'run_backward' / Float32l,
        'swim' / Float32l,
        'swim_backward' / Float32l,
        'turn' / Float32l,
    ),
    'spline_update' / If(
        is_set(c.MovementFlags.SPLINE_ENABLED),
        Struct(
            'flags' / Enum(Int32ul, c.SplineFlags),
            'facing' / If(
                is_set(c.SplineFlags.Final_Point),
                Struct(
                    'x' / Float32l,
                    'y' / Float32l,
                    'z' / Float32l,
                ),
            ),
            'target' / If(
                is_set(c.SplineFlags.Final_Target),
                Int64ul,
            ),
            'angle' / If(
                is_set(c.SplineFlags.Final_Angle),
                Float32l,
            ),
            'time_passed' / Int32ul,
            'duration' / Int32ul,
            'id' / Int32ul,
            'n_points' / Rebuild(Int32ul, lambda this: len(this.points)),
            'points' / GreedyRange(
                Struct(
                    'x' / Float32l,
                    'y' / Float32l,
                    'z' / Float32l,
                )),
            'final_point' / Struct(
                'x' / Float32l,
                'y' / Float32l,
                'z' / Float32l,
            ),
        ),
    ),
)

PositionMovementUpdate = Struct(
    'x' / Float32l,
    'y' / Float32l,
    'z' / Float32l,
    'o' / Float32l,
)

def PackGUID(guid: int) -> dict:
    """Make a PackedGUID dictionary."""
    mask = 0
    guid_bytes = []
    for i, byte in enumerate(guid.to_bytes(8, 'little')):
        if byte != 0:
            mask |= (1 << i)
            guid_bytes.append(byte)

    return dict(
        mask=mask,
        bytes=guid_bytes,
    )

FullUpdateBlock = Struct(
    'guid' / PackedGUID,
    'object_type' / Enum(Int8ul, c.TypeID),
    'flags' / Enum(Int8ul, c.UpdateFlags),
    'movement_update' / Switch(
        lambda this: this.flags,
        cases={
            c.UpdateFlags.LIVING: FullMovementUpdate,
            c.UpdateFlags.HAS_POSITION: PositionMovementUpdate,
        },
    ),
    'high_guid' / If(
        is_set(c.UpdateFlags.HIGHGUID),
        Int32ul,
    ),
    'is_update_all' / If(
        is_set(c.UpdateFlags.ALL),
        Const(b'\x01\x00\x00\x00'),
    ),
    'victim_guid' / If(
        is_set(c.UpdateFlags.FULLGUID),
        PackedGUID,
    ),
    'world_time' / If(
        is_set(c.UpdateFlags.TRANSPORT),
        Int32ul,
    ),
    'update_fields' / UpdateFields,
)

ValuesUpdateBlock = Struct(
    'guid' / PackedGUID,
    'update' / UpdateFields,
)

OutOfRangeUpdateBlock = Struct(
    'n_guids' / Rebuild(Int32ul, lambda this: len(this.guids)),
    'guids' / GreedyRange(PackedGUID),
)

UpdateBlock = Struct(
    'update_type' / Enum(Int8ul, c.UpdateType),
    'update_block' / Switch(
        lambda this: this.update_type,
        cases={
            c.UpdateType.OUT_OF_RANGE_OBJECTS: OutOfRangeUpdateBlock,
            c.UpdateType.VALUES: ValuesUpdateBlock,
        },
        default=FullUpdateBlock,
    ),
)

ServerUpdateObject = Struct(
    'n_blocks' / Rebuild(Int32ul, lambda this: len(this.blocks)),
    'is_transport' / Int8ul,
    'blocks' / GreedyRange(UpdateBlock),
)
