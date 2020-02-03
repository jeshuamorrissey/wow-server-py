from construct import Struct, Int32ul

ServerTutorialFlags = Struct('tutorials' / Int32ul[8])
