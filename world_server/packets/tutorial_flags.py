from construct import Int32ul, Struct

ServerTutorialFlags = Struct('tutorials' / Int32ul[8])
