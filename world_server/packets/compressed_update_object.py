from construct import Compressed, Struct, Int32ul, Rebuild

from world_server.packets.update_object import ServerUpdateObject

ServerCompressedUpdateObject = Struct(
    'uncompressed_size' / Int32ul,
    'data' / Compressed(ServerUpdateObject, 'zlib', level=6),
)
