# Warmup-1 > sleep_in 
def sleep_in(weekday, vacation):
    return not weekday or vacation
print(sleep_in)


# Warmup-1 > diff21
def diff21(n):
  if n > 21:
    return 2 * abs (n - 21)
  else:
    return abs (n - 21)
  

# Warmup-1 > near_hundred
def near_hundred(n):
  abs(n - 100) <= 10 or abs(n - 200) <= 10


# Warmup-1 > missing_char
def missing_char(s, n):
    return s[:n] + s[n+1:]


# Warmup-1 > monkey_trouble
def monkey_trouble(a_smile, b_smile):
  if a_smile and b_smile:
    return True
  if not a_smile and not b_smile:
    return True
  return False


# Warmup-1 > parrot_trouble
def parrot_trouble(talking, hour):
   return (talking and (hour < 7 or hour > 20))


# Warmup-1 > pos_neg
def pos_neg(a, b, negative):
  if negative:
    return (a < 0 and b < 0)
  else:
    return ((a < 0 and b > 0) or (a > 0 and b < 0))
  

# Warmup-1 > front_back
def front_back(str):
    if len(str) <= 1:
        return str
    return str[-1] + str[1:-1] + str[0]


# Warmup-1 > sum_double
def sum_double(a, b):
    if a == b:
        return 2 * (a + b)
    else:
        return a + b
    

# Warmup-1 > makes10
def makes10(a, b):
    return a == 10 or b == 10 or (a + b) == 10


# Warmup-1 > not_string
def not_string(str):
    if str.startswith("not"):
        return str
    else:
        return "not " + str
    

# Warmup-1 > front3
def front3(str):
    front = str[:3]
    return front * 3


# Warmup-2 > string_times
def string_times(str, n):
    return str * n


# Warmup-2 > string_splosion
def string_splosion(str):
    result = ''
    for i in range(len(str)):
        result += str[:i+1]
    return result


# Warmup-2 > array_front9
def array_front9(nums):
    for i in range(min(4, len(nums))):
        if nums[i] == 9:
            return True
    return False


# Warmup-2 > front_times
def front_times(str, n):
    front = str[:3]  
    return front * n


# Warmup-2 > last2
def last2(str):
    if len(str) < 2:
        return 0  # No possible match if string is too short
    last2 = str[-2:]  # get last 2 chars
    count = 0

    for i in range(len(str) - 2):
        if str[i:i+2] == last2:
            count += 1

    return count


# Warmup-2 > array123
def array123(nums):
    for i in range(len(nums) - 2):  # stop 2 elements early
        if nums[i] == 1 and nums[i+1] == 2 and nums[i+2] == 3:
            return True
    return False


# Warmup-2 > string_bits
def string_bits(str):
  return str[::2]  # take every second character, starting at index 0


# Warmup-2 > array_count9
def array_count9(nums):
   return nums.count(9)


# Warmup-2 > string_match
def string_match(a, b):
    count = 0
    # Find the shortest string length - 1 (because we compare 2-letter substrings)
    max_len = min(len(a), len(b)) - 1

    for i in range(max_len + 1):
        if a[i:i+2] == b[i:i+2]:
            count += 1
    return count


# String-1 > hello_name
def hello_name(name):
    return "Hello " + name + "!"


# String-1 > make_out_word
def make_out_word(out, word):
    return out[:2] + word + out[2:]


# String-1 > first_half
def first_half(str):
   return str[:len(str)//2]


# String-1 > non_start
def non_start(a, b):
  return a[1:] + b[1:]


# String-1 > make_abba
def make_abba(a, b):
  return a + b + b + a


# String-1 > extra_end
def extra_end(str):
  return str[-2:] * 3


# String-1 > without_end
def without_end(str):
  return str[1:-1]


# String-1 > left2
def left2(str):
    return str[2:] + str[:2]


# String-1 > make_tags
def make_tags(tag, word):
    return "<" + tag + ">" + word + "</" + tag + ">"


# String-1 > first_two
def first_two(str):
    return str[:2]


# String-1 > combo_string
def combo_string(a, b):
    if len(a) < len(b):
        return a + b + a
    else:
        return b + a + b



# String-2 > double_char
def double_char(s):
    result = ''
    for char in s:
        result += char * 2
    return result


# String-2 > count_code
def count_code(str):
    count = 0
    for i in range(len(str) - 3):
        if str[i] == 'c' and str[i+1] == 'o' and str[i+3] == 'e':
            count += 1
    return count

# String-2 > count_hi
def count_hi(s):
    count = 0
    for i in range(len(s) - 1):
        if s[i:i+2] == 'hi':
            count += 1
    return count


# String-2 > end_other
def end_other(a, b):
    a = a.lower()
    b = b.lower()
    return a.endswith(b) or b.endswith(a)


# String-2 > cat_dog
def cat_dog(str):
  return str.count('cat') == str.count('dog')


# String-2 > xyz_there
def xyz_there(s):
    for i in range(len(s) - 2):
        if s[i:i+3] == 'xyz':
            if i == 0 or s[i-1] != '.':
                return True
    return False


# List-1 > first_last6
def first_last6(nums):
  return nums[0] == 6 or nums[-1] == 6


# List-1 > common_end
def common_end(a, b):
  return a[0] == b[0] or a[-1] == b[-1]


# List-1 > reverse3
def reverse3(nums):
  return nums[::-1]


# List-1 > middle_way
def middle_way(a, b):
  return [a[1], b[1]]


# List-1 > same_first_last
def same_first_last(nums):
  return len(nums) >= 1 and nums[0] == nums[-1]


# List-1 > sum3
def sum3(nums):
  return nums[0] + nums[1] + nums[2]


# List-1 > max_end3
def max_end3(nums):
    max_val = max(nums[0], nums[2])
    return [max_val, max_val, max_val]


# List-1 > make_ends
def make_ends(nums):
  return [nums[0], nums[-1]]


# List-1 > make_pi
def make_pi():
  return [3, 1, 4]


# List-1 > rotate_left3
def rotate_left3(nums):
  return [nums[1], nums[2], nums[0]]


# List-1 > sum2
def sum2(nums):
  if len(nums) >= 2:
     return nums[0] + nums[1]
  elif len(nums) == 1:
    return nums[0]
  else:
    return 0


# List-1 > has23
def has23(nums):
    return 2 in nums or 3 in nums



# List-2 > count_evens
def count_evens(nums):
    count = 0
    for num in nums:
        if num % 2 == 0:
            count += 1
    return count


# List-2 > sum13
def sum13(nums):
    total = 0
    i = 0
    while i < len(nums):
        if nums[i] == 13:
            i += 2  # Skip 13 and the next number
        else:
            total += nums[i]
            i += 1
    return total


# List-2 > big_diff
def big_diff(nums):
    return max(nums) - min(nums)


# List-2 > sum67
def sum67(nums):
    total = 0
    in_block = False 

    for num in nums:
        if in_block:
            if num == 7:
                in_block = False 
        elif num == 6:
            in_block = True 
        else:
            total += num

    return total


# List-2 > centered_average
def centered_average(nums):
    nums_copy = nums[:]  # Copy the list to avoid modifying the original
    
    nums_copy.remove(min(nums_copy))  # Remove one smallest value
    nums_copy.remove(max(nums_copy))  # Remove one largest value
    
    return sum(nums_copy) // len(nums_copy)


# List-2 > has22
def has22(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 2 and nums[i + 1] == 2:
            return True
    return False


# Logic-1 > cigar_party
def cigar_party(cigars, is_weekend):
    if is_weekend:
        return cigars >= 40
    else:
        return 40 <= cigars <= 60


# Logic-1 > caught_speeding
def caught_speeding(speed, is_birthday):
    if is_birthday:
        speed -= 5  # Give 5 mph grace on birthday
    
    if speed <= 60:
        return 0
    elif speed <= 80:
        return 1
    else:
        return 2


# Logic-1 > love6
def love6(a, b):
    return a == 6 or b == 6 or (a + b) == 6 or abs(a - b) == 6


# Logic-1 > date_fashion
def date_fashion(you, date):
    if you <= 2 or date <= 2:
        return 0
    elif you >= 8 or date >= 8:
        return 2
    else:
        return 1


# Logic-1 > sorta_sum
def sorta_sum(a, b):
    s = a + b
    if 10 <= s <= 19:
        return 20
    else:
        return s


# Logic-1 > in1to10
def in1to10(n, outside_mode):
    if outside_mode:
        return n <= 1 or n >= 10
    else:
        return 1 <= n <= 10


# Logic-1 > squirrel_play
def squirrel_play(temperature, is_summer):
    upper_limit = 100 if is_summer else 90
    return 60 <= temperature <= upper_limit


# Logic-1 > alarm_clock
def alarm_clock(day, vacation):
    if vacation:
        if day == 0 or day == 6:  # weekend
            return "off"
        else:  # weekday
            return "10:00"
    else:
        if day == 0 or day == 6:  # weekend
            return "10:00"
        else:  # weekday
            return "7:00"


# Logic-1 > near_ten
def near_ten(num):
    remainder = num % 10
    return remainder <= 2 or remainder >= 8


# Logic-2 > make_bricks
def make_bricks(small, big, goal):
    max_big_used = min(big, goal // 5)
    remaining = goal - (max_big_used * 5)
    return small >= remaining



# Logic-2 > no_teen_sum
def no_teen_sum(a, b, c):
    def fix_teen(n):
        if n in [13, 14, 17, 18, 19]:
            return 0
        return n

    return fix_teen(a) + fix_teen(b) + fix_teen(c)



# Logic-2 > make_chocolate
def make_chocolate(small, big, goal):
    big_used = min(goal // 5, big)
    remaining = goal - big_used * 5
    if small >= remaining:
        return remaining
    else:
        return -1


# Logic-2 > lone_sum
def lone_sum(a, b, c):
    total = 0
    if a != b and a != c:
        total += a
    if b != a and b != c:
        total += b
    if c != a and c != b:
        total += c
    return total


# Logic-2 > round_sum
def round_sum(a, b, c):
    return round10(a) + round10(b) + round10(c)

def round10(num):
    if num % 10 >= 5:
        return ((num // 10) + 1) * 10
    else:
        return (num // 10) * 10



# Logic-2 > lucky_sum
def lucky_sum(a, b, c):
    if a == 13:
        return 0
    elif b == 13:
        return a
    elif c == 13:
        return a + b
    else:
        return a + b + c



# Logic-2 > close_far
def close_far(a, b, c):
    close_b = abs(a - b) <= 1
    close_c = abs(a - c) <= 1
    far_b = abs(a - b) >= 2 and abs(b - c) >= 2
    far_c = abs(a - c) >= 2 and abs(b - c) >= 2

    return (close_b and far_c) or (close_c and far_b)
