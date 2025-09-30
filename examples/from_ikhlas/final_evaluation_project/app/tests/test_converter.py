from app.converter import convert_measurements

def test_examples():
    assert convert_measurements("aa") == [1]
    assert convert_measurements("abbcc") == [2, 6]
    assert convert_measurements("dz_a_aazzaaa") == [28, 53, 1]
    assert convert_measurements("abcdabcdab") == [2, 7, 7]
    assert convert_measurements("abcdabcdab_") == [2, 7, 7, 0]
    assert convert_measurements("zdaaaaaaaabaaaaaaaabaaaaaaaabbaa") == [34]
    assert convert_measurements("zza_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_") == [26]
    assert convert_measurements("za_a_a_a_a_a_a_a_a_a_a_a_a_azaaa") == [40, 1]
