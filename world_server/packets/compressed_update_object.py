from construct import Compressed

from world_server.packets.update_object import ServerUpdateObject

ServerCompressedUpdateObject = Compressed(ServerUpdateObject, 'zlib', level=6)
