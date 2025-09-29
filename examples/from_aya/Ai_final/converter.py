def char_to_value(ch: str) -> int:
    if ch == "_":
        return 0
    return ord(ch) - ord("a") + 1


def read_element(s, i):
    if s[i] == "z":
        total = 0
        while i < len(s) and s[i] == "z":
            total += 26
            i += 1
        if i < len(s):
            total += char_to_value(s[i])
            i += 1
        return total, i
    else:
        return char_to_value(s[i]), i + 1


def convert_measurements(input_str: str):
    results = []
    i = 0
    n = len(input_str)

    while i < n:
        count, i = read_element(input_str, i)

        if count == 0:
            results.append(0)
            continue

        total = 0
        for _ in range(count):
            if i >= n:
                break
            val, i = read_element(input_str, i)
            total += val

        results.append(total)

    return results
