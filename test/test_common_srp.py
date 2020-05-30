import math

from common import srp


def test_random():
    assert math.ceil(srp.Random(32).bit_length() / 8) == 32
    assert math.ceil(srp.Random(16).bit_length() / 8) == 16


def test_hex_to_int_even_length_strings():
    assert srp.HexToInt('FF000000', 'big') == 4278190080
    assert srp.HexToInt('000000FF', 'little') == 4278190080


def test_hex_to_int_odd_length_strings():
    assert srp.HexToInt('00000FF', 'little') == 4278190080
    assert srp.HexToInt('FF00000', 'big') == 4278190080


def test_int_to_bytes():
    assert srp.IntToBytes(1) == b'\x01'
    assert srp.IntToBytes(256) == b'\x01\x00'


def test_hash():
    assert srp._H(1, b'234', bytearray(b'567'), '890') == 1
