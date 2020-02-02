from construct import Int32ul, Struct

ServerPong = Struct('pong' / Int32ul)
