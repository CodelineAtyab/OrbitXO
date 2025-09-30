def char_to_value(ch):
    if ch == "_":
        return 0
    return ord(ch) - ord('a') + 1

def tokenize(s):
    tokens, i = [], 0
    while i < len(s):
        if s[i] == "z":
            z_count = 0
            while i < len(s) and s[i] == "z":
                z_count += 1
                i += 1
            if i < len(s):
                tokens.append(z_count * 26 + char_to_value(s[i]))
                i += 1
            else:
                tokens.append(z_count * 26)
        else:
            tokens.append(char_to_value(s[i]))
            i += 1
    return tokens

def decode_string(s):
    tokens, result, i = tokenize(s), [], 0
    while i < len(tokens):
        count = tokens[i]
        if count == 0:
            result.append(0)
            i += 1
            continue
        values = tokens[i+1:i+1+count]
        result.append(sum(values))
        i += count + 1
    return result
