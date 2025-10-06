#package converter

#convert single string to number value
def char_to_value(ch: str) -> int:
    if ch == "_":
        return 0
    return ord(ch) - ord("a") + 1

#handle 'z' 
def take_z_chain(s: str, i: int) -> tuple[int, int]:
    total = 0
    while i < len(s) and s[i] == "z":
        total += 26
        i += 1
    if i < len(s):  # attach next char
        total += char_to_value(s[i])
        i += 1
    return total, i

#converts measurement string to list
def convert_measurements(input_str: str) -> list[int]:
    results = []
    i = 0
    n = len(input_str)

    # handle "_" string
    if n > 0 and input_str[0] == "_":
        return [0]

    while i < n:
        # handle count
        if input_str[i] == "_":
            # if "_" as COUNT
            if (not results) or results[-1] != 0:  #prevent duplicates
                results.append(0)
            i += 1
            continue

        if input_str[i] == "z":
            count, i = take_z_chain(input_str, i)
        else:
            count = char_to_value(input_str[i])
            i += 1

        # collect/sum the package values
        total = 0
        elements_taken = 0
        while elements_taken < count and i < n:
            if input_str[i] == "_":
                total += 0
                i += 1
            elif input_str[i] == "z":
                val, i = take_z_chain(input_str, i)
                total += val
            else:
                total += char_to_value(input_str[i])
                i += 1
            elements_taken += 1

        results.append(total)

        #trailing "_" as COUNT
        if i == n - 1 and input_str[i] == "_":
            if results[-1] != 0:  #avoid duplicate zeros
                results.append(0)
            i += 1

    return results
