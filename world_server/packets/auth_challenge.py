from construct import Int32ub, Struct

ServerAuthChallenge = Struct('seed' / Int32ub)
