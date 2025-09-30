from parser import parse_measurement

tests = {
    "aa": [1],
    "abbcc": [2, 6],
    "dz_a_aazzaaa": [28, 53, 1],
    "a_": [0],
    "abcdabcdab": [2, 7, 7],
    "abcdabcdab_": [2, 7, 7, 0],
    "azaz_aa": [27, 2],  
    "z_": [0],
    "zz_": [26],
}

for input_str, expected in tests.items():
    result = parse_measurement(input_str)
    print(f"Input: {input_str}\nOutput: {result}\nExpected: {expected}\nMatch: {result == expected}\n")
