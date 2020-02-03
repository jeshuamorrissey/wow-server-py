from construct import Int32ul, Struct

ServerAccountDataTimes = Struct('data_times' / Int32ul[32])
