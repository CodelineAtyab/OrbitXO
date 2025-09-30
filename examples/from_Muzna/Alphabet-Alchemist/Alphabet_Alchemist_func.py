def char_to_value(ch: str) -> int:
    """Convert a single character to its numeric value."""
    if ch == "_":
        return 0
    return ord(ch) - ord("a") + 1


def parse_element(s: str, i: int) -> tuple[int, int]:
    """
    Parse one element starting at index i.
    Handles rule that 'z' cannot stand alone.
    Returns (value, new_index).
    """
    if s[i] == "z":
        total = 0
        while i < len(s) and s[i] == "z":
            total += 26
            i += 1
        if i < len(s):  # attach the next non-z
            total += char_to_value(s[i])
            i += 1
        return total, i
    else:
        return char_to_value(s[i]), i + 1


def convert_measurements(s: str) -> list[int]:
    """Main conversion function following all rules."""
    if not s:
        return []

    # Rule 8: if input starts with "_", only append [0]
    if s[0] == "_":
        return [0]

    output = []
    i = 0
    n = len(s)

    while i < n:
        # Parse count element
        count, i = parse_element(s, i)

        if count == 0:  # "_" as count
            output.append(0)
            continue

        # Collect count elements
        total = 0
        for _ in range(count):
            if i >= n:
                break
            val, i = parse_element(s, i)
            total += val
        output.append(total)

    return output

if __name__ == "__main__":
    print(convert_measurements("aa"))                     # [1]
    print(convert_measurements("abbcc"))                  # [2, 6]
    print(convert_measurements("dz_a_aazzaaa"))           # [28, 53, 1]
    print(convert_measurements("a_"))                     # [0]
    print(convert_measurements("abcdabcdab"))             # [2, 7, 7]
    print(convert_measurements("abcdabcdab_"))            # [2, 7, 7, 0]
    print(convert_measurements("zdaaaaaaaabaaaaaaaabaaaaaaaabbaa"))  # [34]
    print(convert_measurements("zza_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_")) # [26]
    print(convert_measurements("za_a_a_a_a_a_a_a_a_a_a_a_a_azaaa")) # [40, 1]
    print(convert_measurements("_"))                       # [0]
    print(convert_measurements("_ad"))                    # [0]
    print(convert_measurements("_zzzb"))                  # [0]
    print(convert_measurements("__"))                     # [0]