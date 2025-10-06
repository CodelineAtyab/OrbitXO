from typing import List, Tuple

def _get_char_value(char: str) -> int:
    
    if 'a' <= char <= 'z':
        return ord(char) - ord('a') + 1
    return 0

def _parse_count(s: str, index: int) -> Tuple[int, int]:
    
    count = 0
    while index < len(s) and s[index] == 'z':
        count += 26
        index += 1
    
    if index < len(s):
        count += _get_char_value(s[index])
        index += 1
    return count, index

def _process_segment(s: str, index: int) -> Tuple[int, int]:
    
    count, index = _parse_count(s, index)
    
    sub_chars_end_index = index
    items_to_collect = count
    
    while items_to_collect > 0 and sub_chars_end_index < len(s):
        if s[sub_chars_end_index] == 'z':
            
            temp_index = sub_chars_end_index
            while temp_index < len(s) and s[temp_index] == 'z':
                temp_index += 1
            if temp_index < len(s):
                temp_index += 1
            sub_chars_end_index = temp_index
        else:
            sub_chars_end_index += 1
        items_to_collect -= 1

    sub_chars = s[index:sub_chars_end_index]
    current_sum = sum(_get_char_value(c) for c in sub_chars)
    return current_sum, sub_chars_end_index

def string_to_number_list(s: str) -> List[int]:
    
    s = s.lower()
    result = []
    i = 0
    while i < len(s):
        if _get_char_value(s[i]) == 0:
            result.append(0)
            i += 1
        else:
            current_sum, i = _process_segment(s, i)
            result.append(current_sum)
    return result
