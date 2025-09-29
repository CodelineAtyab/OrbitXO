def convert_measurements(input_str: str):
    """
    يحول النصوص إلى أرقام حسب القواعد:
    1. a=1, b=2, ..., z=26
    2. '_' = 0
    3. 'z' لا يمكن أن تكون لوحدها، لازم تاخذ الحرف اللي بعدها (حتى لو كان 'z' أو '_')
    4. أول عنصر في كل package هو count (عدد العناصر اللي بعدها)
    5. لو count = '_' (يعني 0) → أضف 0 مباشرة
    6. لو string ينتهي بـ '_' وكان count → أضف 0
       أما لو '_' كقيمة → تحسب مع باقي القيم
    """

    # دالة لتحويل حرف/مجموعة أحرف إلى قيمة رقمية
    def char_to_value(seq: str) -> int:
        total = 0
        for c in seq:
            if c == "_":
                total += 0
            else:
                total += ord(c) - 96  # ord('a')=97 => a=1, b=2...
        return total

    results = []
    i = 0
    n = len(input_str)

    while i < n:
        # --------- 1) استخراج count -----------
        if input_str[i] == "_":
            count = 0
            results.append(0)
            i += 1
            continue

        # حالة 'z' كـ count
        if input_str[i] == "z":
            seq = "z"
            j = i + 1
            while j < n and input_str[j] == "z":
                seq += "z"
                j += 1
            if j < n:
                seq += input_str[j]
                j += 1
            count = char_to_value(seq)
            i = j
        else:
            count = char_to_value(input_str[i])
            i += 1

        # --------- 2) استخراج value(s) -----------
        if count == 0:
            results.append(0)
            continue

        values = []
        taken = 0
        while taken < count and i < n:
            if input_str[i] == "z":
                seq = "z"
                j = i + 1
                while j < n and input_str[j] == "z":
                    seq += "z"
                    j += 1
                if j < n:
                    seq += input_str[j]
                    j += 1
                values.append(char_to_value(seq))
                i = j
            else:
                values.append(char_to_value(input_str[i]))
                i += 1
            taken += 1

        results.append(sum(values))

    return results


# ------------------- للتجربة -------------------
if __name__ == "__main__":
    tests = [
        ("aa", [1]),
        ("abbcc", [2, 6]),
        ("dz_a_aazzaaa", [28, 53, 1]),
        ("a_", [0]),
        ("abcdabcdab", [2, 7, 7]),
        ("abcdabcdab_", [2, 7, 7, 0]),
        ("zdaaaaaaaabaaaaaaaabaaaaaaaabbaa", [34]),
        ("zza_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_a_", [26]),
        ("za_a_a_a_a_a_a_a_a_a_a_a_a_azaaa", [40, 1]),
    ]

    for s, expected in tests:
        result = convert_measurements(s)
        print(f"Input: {s} → Output: {result} | Expected: {expected}")
