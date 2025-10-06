import pytest
from decoder import decode

def test_examples():
    assert decode("aa") == [1]
    assert decode("abbcc") == [2, 6]
    assert decode("dz_a_aazzaaa") == [28, 53, 1]
    assert decode("a_") == [0]
    assert decode("abcdabcdab") == [2, 7, 7]
    assert decode("abcdabcdab_") == [2, 7, 7, 0]
    assert decode("zdaaaaaaaabaaaaaaaabaaaaaaaabbaa") == [34]
    assert decode("zza_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_") == [26]
    assert decode("za_a_a_a_a_a_a_a_a_a_a_a_a_azaaa") == [40, 1]
