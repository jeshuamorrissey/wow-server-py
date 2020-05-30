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
    assert srp._H(1, b'234', bytearray(b'567'), '890') == 30199234954775863460339964203552832472377371615


def test_generate_verifier():
    assert srp.GenerateVerifier('account', 'pass',
                                12345) == 25407694043095608746006544038789124829486757109212090961649910872471066201086


def test_generate_ephemeral(mocker):
    mock_random = mocker.patch.object(srp, 'Random', return_value=10)

    b, B = srp.GenerateEphemeral(1234)
    assert b == 10
    assert B == 282478951
    assert mock_random.mock_calls == [mocker.call(19)]


def test_calculate_session_key():
    K, M = srp.CalculateSessionKey(1, 2, 3, 4, 5, 'name')
    assert K == 652374140347660906080245677135003171278246154842732112156776516119877651028025349268763470095311
    assert M == 699372769848255409099403746491956139238464387117


def test_calculate_server_proof():
    assert srp.CalculateServerProof(1, 2, 3) == 1186741094938957921710144549567755328213087172464


def test_calculate_auth_session_proof():
    assert srp.CalculateAuthSessionProof('name', 1, 2, 3, 4) == 1358367678460761507410566424216791441885924568110
