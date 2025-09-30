# parser.py

def char_to_value(c: str) -> int:
    """Convert letter to number: a=1, ..., z=26, _=0."""
    if c == '_':
        return 0
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    return 0


def parse_measurement(input_str: str) -> list[int]:
    """
    Parse measurement string into list of package totals.

    Rules enforced:
    - First letter = count of logical "letters" to sum for this package.
    - '_' is a standalone package (value 0) when encountered at package start.
    - If a letter in the payload is 'z', treat the entire run of consecutive 'z's
      AND the very next character (if present) as one logical unit to be added.
    """
    packages = []
    i = 0
    n = len(input_str)

    while i < n:
        if input_str[i] == '_':
            packages.append(0)
            i += 1
            continue

        # number of logical letters to take for this package
        count = char_to_value(input_str[i])
        i += 1

        total = 0
        letters_taken = 0

        while letters_taken < count and i < n:
            # If we encounter 'z', consume the run of z's and also include
            # the very next character (if exists) as part of the same logical unit.
            if input_str[i] == 'z':
                # collect consecutive z's
                j = i
                while j < n and input_str[j] == 'z':
                    j += 1
                # sum the z-run
                combined = sum(char_to_value(input_str[k]) for k in range(i, j))
                # include the immediate next character after the z-run, if any
                if j < n:
                    combined += char_to_value(input_str[j])
                    j += 1
                total += combined
                i = j
            else:
                # regular letter or underscore
                total += char_to_value(input_str[i])
                i += 1

            letters_taken += 1

        packages.append(total)

    return packages