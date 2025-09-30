def char_to_value(c):
    """Convert character to numeric value (a=1,...,z=26, _=0)"""
    return 0 if c == '_' else ord(c) - ord('a') + 1

def get_next_element(s, index):
    """Get next element considering z rule"""
    if s[index] != 'z':
        return s[index], index + 1
    # z rule: take z(s) + next char
    start = index
    while index < len(s) and s[index] == 'z':
        index += 1
    if index < len(s):
        index += 1  # include next char after z sequence
    return s[start:index], index

def get_package_count(s):
    """Get package count value considering z rule"""
    if not s:
        return 0, ''
    elem, idx = get_next_element(s, 0)
    count_value = sum(char_to_value(ch) for ch in elem)
    return count_value, s[idx:]

def get_package_value(s, count):
    """Get package value summing exactly 'count' values (not just elements)"""
    value = 0
    idx = 0
    values_taken = 0

    while values_taken < count and idx < len(s):
        elem, next_idx = get_next_element(s, idx)
        elem_value = sum(char_to_value(ch) for ch in elem)
        value += elem_value
        idx = next_idx
        values_taken += 1  # عد القيم بدقة
    return value, s[idx:]

def convert_measurements(s):
    result = []
    while s:
        # Get package count
        count, s = get_package_count(s)
        if count == 0 and not s:
            result.append(0)
            break
        # Get package value
        if s:
            value, s = get_package_value(s, count)
        else:
            value = 0
        result.append(value)
    return result

# Test function
def test_convert_measurements():
    test_cases = [
        ("aa", [1]),
        ("abbcc", [2, 6]),
        ("dz_a_aazzaaa", [28, 53, 1]),
        ("a_", [0]),
        ("abcdabcdab", [2, 7, 7]),
        ("abcdabcdab_", [2, 7, 7, 0]),
        ("zdaaaaaaaabaaaaaaaabaaaaaaaabbaa", [34]),
        ("zza_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_", [26]),
        ("za_a_a_a_a_a_a_a_a_a_a_a_a_azaaa", [40, 1])
    ]
    
    print("Testing convert_measurements function:")
    print("=" * 50)
    
    for i, (input_str, expected) in enumerate(test_cases, 1):
        result = convert_measurements(input_str)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"Test {i}: {status}")
        print(f"  Input: '{input_str}'")
        print(f"  Expected: {expected}")
        print(f"  Got: {result}")
        if result != expected:
            print(f"  ERROR: Results don't match!")
        print()

if __name__ == "__main__":
    test_convert_measurements()
