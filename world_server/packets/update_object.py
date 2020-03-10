# type: ignore[operator]

import enum
import struct

from construct import (Adapter, Array, Byte, Bytes, Const, Debugger, Enum, Float32l, GreedyBytes, GreedyRange, If,
                       IfThenElse, Int8ul, Int32ul, Int64ul, Rebuild, Struct, Switch)

from database import constants, game, world


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

        return (hex(guid & 0xFFFFFFFF), hex(guid >> 32))

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
        num_fields = obj['num_fields']

        # Calculate the number of mask blocks we need.
        blocks = (num_fields + 32 - 1) // 32

        # Each mask block is 4 bytes long
        num_bytes = blocks * 4

        mask = 0
        fields = []
        for field, value in sorted(obj['fields'].items()):
            if value is None:
                continue

            mask |= (1 << field)
            if isinstance(value, world.GUID):
                mask |= (1 << (field + 1))
                fields.append(value.low.to_bytes(4, 'little'))
                fields.append(value.high.to_bytes(4, 'little'))
            elif isinstance(value, int):
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


UpdateFields = UpdateFieldsAdapter(
    Struct(
        'blocks' / Int8ul,
        'masks' / Array(lambda this: this.blocks * 4, Byte),
        'fields' / Array(lambda this: sum(bin(m).count('1') for m in this.masks), Bytes(4)),
    ))

is_set = lambda enum: lambda this: enum & this.flags
is_not_set = lambda enum: lambda this: not (enum & this.flags)

FullMovementUpdate = Struct(
    'flags' / Int32ul,
    'time' / Int32ul,
    'x' / Float32l,
    'y' / Float32l,
    'z' / Float32l,
    'o' / Float32l,
    'transport' /
    If(is_set(game.MovementFlags.ONTRANSPORT),
       Struct(
           'guid' / Int64ul,
           'x' / Float32l,
           'y' / Float32l,
           'z' / Float32l,
           'o' / Float32l,
           'time' / Int32ul,
       )),
    'swimming' / If(
        is_set(game.MovementFlags.SWIMMING),
        Struct('pitch' / Float32l),
    ),
    'last_fall_time' / If(
        is_not_set(game.MovementFlags.ONTRANSPORT),
        Int32ul,
    ),
    'falling' / If(
        is_set(game.MovementFlags.FALLING),
        Struct(
            'velocity' / Float32l,
            'sin_angle' / Float32l,
            'cos_angle' / Float32l,
            'xy_speed' / Float32l,
        ),
    ),
    'spline_elevation' / If(
        is_set(game.MovementFlags.SPLINE_ELEVATION),
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
        is_set(game.MovementFlags.SPLINE_ENABLED),
        Struct(
            'flags' / Int32ul,
            'facing' / If(
                is_set(game.SplineFlags.Final_Point),
                Struct(
                    'x' / Float32l,
                    'y' / Float32l,
                    'z' / Float32l,
                ),
            ),
            'target' / If(
                lambda this: this.flags & game.SplineFlags.Final_Point and not (this.flags & game.SplineFlags.
                                                                                Final_Target),
                Int64ul,
            ),
            'angle' / If(
                lambda this: this.flags & game.SplineFlags.Final_Angle and not (
                    this.flags & game.SplineFlags.Final_Point) and not (this.flags & game.SplineFlags.Final_Target),
                Float32l,
            ),
            'time_passed' / Int32ul,
            'duration' / Int32ul,
            'id' / Int32ul,
            'n_points' / Int32ul,
            'points' / Array(lambda this: this.n_points, Struct(
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
    'object_type' / Int8ul,
    'flags' / Int8ul,
    'movement_update' / IfThenElse(
        is_set(game.UpdateFlags.LIVING),
        FullMovementUpdate,
        If(
            is_set(game.UpdateFlags.HAS_POSITION),
            PositionMovementUpdate,
        ),
    ),
    'high_guid' / If(
        is_set(game.UpdateFlags.HIGHGUID),
        Int32ul,
    ),
    'is_update_all' / If(
        is_set(game.UpdateFlags.ALL),
        Const(int(1).to_bytes(4, 'little')),
    ),
    'victim_guid' / If(
        is_set(game.UpdateFlags.FULLGUID),
        PackedGUID,
    ),
    'world_time' / If(
        is_set(game.UpdateFlags.TRANSPORT),
        Int32ul,
    ),
    'update_fields' / UpdateFields,
)

ValuesUpdateBlock = Struct(
    'guid' / PackedGUID,
    'update' / UpdateFields,
)

OutOfRangeUpdateBlock = Struct(
    'n_guids' / Int32ul,
    'guids' / Array(lambda this: this.n_guids, PackedGUID),
)

UpdateBlock = Struct(
    'update_type' / Int8ul,
    'update_block' / Switch(
        lambda this: this.update_type,
        cases={
            game.UpdateType.OUT_OF_RANGE_OBJECTS: OutOfRangeUpdateBlock,
            game.UpdateType.VALUES: ValuesUpdateBlock,
        },
        default=FullUpdateBlock,
    ),
)

ServerUpdateObject = Struct(
    'n_blocks' / Int32ul,
    'is_transport' / Int8ul,
    'blocks' / Array(lambda this: this.n_blocks, UpdateBlock),
)
