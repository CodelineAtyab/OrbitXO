import pytest
from decoder import decode_string

@pytest.mark.parametrize("input_str, expected", [
    ("aa", [1]),
    ("abbcc", [2, 6]),
    ("dz_a_aazzaaa", [28, 53, 1]),
    ("a_", [0]),
    ("abcdabcdab", [2, 7, 7]),
    ("abcdabcdab_", [2, 7, 7, 0]),
    ("zdaaaaaaaabaaaaaaaabaaaaaaaabbaa", [34]),
    ("zza_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_", [26]),
    ("za_a_a_a_a_a_a_a_a_a_a_a_a_azaaa", [40, 1]),
])
def test_decode_string(input_str, expected):
    assert decode_string(input_str) == expected
