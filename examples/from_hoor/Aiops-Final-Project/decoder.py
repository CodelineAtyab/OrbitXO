def char_to_value(ch: str) -> int:
    if ch == "_":
        return 0
    return ord(ch) - ord("a") + 1

def parse_element(s: str, i: int) -> (int, int):
    if s[i] == "z":
        j = i
        val = 0
        while j < len(s) and s[j] == "z":
            val += 26
            j += 1
        if j < len(s):
            val += char_to_value(s[j])
            j += 1
        return val, j
    else:
        return char_to_value(s[i]), i + 1

def decode(input_str: str) -> list[int]:
    results = []
    i = 0
    n = len(input_str)

    while i < n:
        if input_str[i] == "_":
            results.append(0)
            i += 1
            continue
        count, i = parse_element(input_str, i)
        total = 0
        taken = 0
        while taken < count and i < n:
            val, i = parse_element(input_str, i)
            total += val
            taken += 1
        if count > 0:
            results.append(total)
    return results
