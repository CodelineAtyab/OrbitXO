# sleepin task 
#warmup1 Tasks !!!
def sleep_in(weekday, vacation):
  if not weekday or vacation:
    return True
  else:
    return False
  
#deff task
def diff21(n):
    if n <= 21:
        return (21- n)
    else:
        return(n - 21) * 2
  
#near_hundered
def near_hundred(n):
  return((abs(100-n) <= 10) or (abs(200-n) <=10 ))

#missing char task
def missing_char(str, n):
  front = str[:n]
  back = str[n+1:]
  return front+back

#front_back
def front_back(str):
  if len(str) <= 1:
    return str
    
  mid = str[1:len(str)-1]
    
  return str[len(str)-1] + mid + str[0]
  
#monkey trouble
def monkey_trouble(a_smile, b_smile):
  return (a_smile and b_smile or not a_smile and not b_smile)

#parrot_trouble
def parrot_trouble(talking, hour):
  return talking and (hour < 7 or hour > 20)

#def_neg
def pos_neg(a, b, negative):
    if negative:
        return a < 0 and b < 0
    else:
        return (a < 0 and b > 0) or (a > 0 and b < 0)

#sum_double
def sum_double(a, b):
  if a == b:
    return (a+b)  * 2
  else:
    return a+b
  
#makes10
def makes10(a, b):
      return (a == 10 or b == 10) or (a + b == 10)

#not_string task 
def not_string(str):
  if str.startswith("not"):
    return str
  else:
    return ("not " + str)

#front3
def front3(str):
    if len(str) < 3:
      return str[:3] * 3
    else:
      return (str[:3] * 3)
    
#string Tasks!!!
#string-1 
def hello_name(name):
  return "Hello " + name + "!"

#make-out-word
def make_out_word(out, word):
    middle = out[:2] + word + out[2:]
    return middle

#first-half
def first_half(str):
  return str[:len(str)//2]

#non-start
def non_start(a, b):
  return a[1::] + b[1::]

#make_abba
def make_abba(a, b):
  return a[::] + b[::] + b[::] + a[::]

#extra-end
def extra_end(str):
  if len(str) <= 2:
    return str[-2::] * 3
  else:
    return str[-2::] * 3
  
#without-end
def without_end(str):
    return str[1:len(str)-1]

#left2
def left2(str):
  if len(str) <= 2:
    return str
    
  else:
      
      return str[2:] + str[:2]
#make tags
def make_tags(tag, word):
  return "<" + tag[0::] +">" + word[0:] + "</" + tag[0::] + ">"

#first two
def first_two(str):
  if len(str) < 2:
    return str
  else:
    return str[0:2]

#combo-string
def combo_string(a, b):
  if len(a) < len(b):
    return a + b + a
  else:
      return b + a + b

  #Logic - 1 tasks
  #squarls party
def cigar_party(cigars, is_weekend):
 if is_weekend:
    return cigars >= 40
 else:
    return 40 <= cigars <= 60

#caugt-speeding
def caught_speeding(speed, is_birthday):
  
  if is_birthday and speed <= 65:
      return 0
  elif 66 <= speed <= 85 and is_birthday:
      return 1
  elif speed >= 85 and is_birthday:
      return 2
      
  if not is_birthday and speed <= 60:
        return 0
      
  elif 61 <= speed <= 80 and not is_birthday:
        return 1
        
  elif speed >= 81 and not is_birthday:
    
        return 2
  
#love6
def love6(a, b):
  return a == 6 or b == 6 or (a + b == 6 ) or (b - a == 6) or (a - b == 6)

#data_fashion 
def date_fashion(you, date):
  if you <= 2 or date <= 2:
    return 0
  elif you >= 8 or date >= 8:
    return 2
  else:
    return 1
#sorta sum
def sorta_sum(a, b):
  h = a + b
  if 10 <= h <= 19:
    return 20
  else:
    return h
  
#in1to10
def in1to10(n, outside_mode):
  if outside_mode:
        return n <= 1 or n >= 10
  else:
        return 1 <= n <= 10
  
#squirrel_play 
def squirrel_play(temp, is_summer):
  if 60 <= temp <= 100 and is_summer:
    return True
  elif 60 <= temp <= 90 and not is_summer:
    return True
  else:
    return False

#alarm clock
def alarm_clock(day, vacation):
    if vacation:
        if day == 0 or day == 6:
            return "off"
        else:
            return "10:00"
    else:
        if day == 0 or day == 6:
            return "10:00"
        else:
            return "7:00"

#near10

def near_ten(num):
    if num % 10 in (0, 1, 2, 8, 9):
        return True
    else:
        return False
#double char
def double_char(str):
    list_of_char = list(str)
    comb_char=[]
    for char in list_of_char:
      comb_char.append(char * 2)
    result_char = ''.join(comb_char)
    return result_char


#count_code
def count_code(str):
    count = 0
    for i in range(len(str) - 3):
        if str[i] == 'c' and str[i+1] == 'o' and str[i+3] == 'e':
            count += 1
    return count

#count_hi
def count_hi(str):
  return str.count("hi")

#end_other
def end_other(a, b):
  a = a.lower()
  b = b.lower()
  
  if a.endswith(b):
    return True
  elif b.endswith(a):
    return True
  else:
    return False

#cat_dog
def cat_dog(str):
  if str.count("cat") == str.count("dog"):
    return True
  else:
    return False

#xyz_here
def xyz_there(str):
  this= False
  if 'xyz' in str :
    if len(str) == 3:
      this = True
    for i in range(len(str)- 3):
       if str[i] == "." and (str[i+1] == "x" and str[i+2] == "y" and str [i+3] == "z"):
         this= False
       else:
         this= True
  return this

#warmup 2 
#string times

def string_times(str, n):
  
  return str[::] * n

#front time
def front_times(str, n):
  front = str[0:3]
  if len(str) <= 3:
    return front * n
  else:
    return front * n

#string bits
def string_bits(str):
  if len(str) >= 10:
    return str[0::2]
  else:
    return str[0::2]
  
#string splosion
def string_splosion(str):
  result = ""
  for i in range(0,len(str)+1):
    result += str[:i]
  return result

#last 2
def last2(str):
  if len(str) < 2:
    return 0
  last2 = str[len(str)-2:]
  count = 0
  for i in range(len(str)-2):
    sub = str[i:i+2]
    if sub == last2:
      count = count + 1

  return count

#array_count9
def array_count9(nums):
  return nums.count(9)

#array front 9
def array_front9(nums):
  x = False
  if len(nums) >= 4:
   if nums[0] == 9 or (nums[1] == 9 or nums[2] == 9 or nums[3] == 9):
      x = True
   else:
      x = False 
  elif 9 in nums:
    x = True
  else:
    x = False
  return x
    
#array123
def array123(nums):
  for i in range (len(nums)-2):
    if (nums[i] == 1 and nums[i+1] == 2 and nums[i+2] == 3):
      return True
  return False

#string match
def string_match(a, b):
  shorter = min(len(a), len(b))
  count = 0
  
  for i in range(shorter-1):
    a_sub = a[i:i+2]
    b_sub = b[i:i+2]
    if a_sub == b_sub:
      count = count + 1

  return count

#list1 tasks
#first_last6
def first_last6(nums):
  if len(nums) >= 1:
    if nums[0] == 6 or nums[len(nums)-1] == 6:
      return True
    else:
      return False
  else:
    return False
  
#same_first_last
def same_first_last(nums):
  if len(nums) >= 1:
    if nums[0] == nums[len(nums)-1]:
      return True
    else:
       return False
  else:
    return False

#make_pi
def make_pi():
  make_pi = [3,1,4]
  return make_pi

#common_end
def common_end(a, b):
  if len(a) >= 1:
    if a[0] == b[0] or a[len(a)-1] == b[len(b)-1]:
      return True
    else:
      return False
    
#sum3
def sum3(nums):
  return sum(nums)

#rotate_left3
def rotate_left3(nums):
  
    new_list = [nums[1],nums[2],nums[0]]
     
    return new_list

#reverse 3
def reverse3(nums):
  
  new_list = [nums[2],nums[1],nums[0]]
  
  return new_list

#max_end3
def max_end3(nums):
  
  first_element = nums[0]
  last_element = nums[len(nums)-1]
  
  if first_element  > last_element or last_element > first_element or first_element == last_element:
    
    if first_element >= last_element:
      new_list = [first_element] * 3
      return new_list
      
    elif last_element >= first_element:
      return [last_element] * 3

#sum2
def sum2(nums):
  
  if len(nums) >= 2:
    
    return nums[0] + nums[1]
    
  elif len(nums) == 1:
    
    c = nums[0]
    return c
  
  elif len(nums) == 0:
    return 0
  
  #middle_way
def middle_way(a, b):
  
  return [a[1],b[1]]

#make_end
def make_ends(nums):
  
  return [nums[0],nums[len(nums)-1]]

#has23

def has23(nums):
  if nums[0] == 2 or nums[0] == 3 or  nums[1] == 2 or nums[1] == 3:
    return True
  else:
    return False

#logic-2 tasks
#make_bricks
def make_bricks(small, big, goal):
  
  min_break = min(goal // 5,big)
  remaining = goal - (min_break * 5)
  
  return remaining <= small

#long sum
def lone_sum(a, b, c):
  if a == b or a == c or b == a or b == c or c == a or c == b :
    if a != b and a!=c:
      return a
    elif b != a and b !=c:
      return b
    elif c != a and c!=b:
      return c
    elif c == b == a:
      return 0
  else:
    return a+b+c
  
  #lucky sum
def lucky_sum(a, b, c):
  
  if a == 13:
    return 0
  elif b == 13:
      return a
  elif c == 13:
      return a+b
  else:
      return a + b + c
  
  #fix teen
def fix_teen(n):
    if 13 <= n <= 19 and n not in (15, 16):
        return 0
    return n

def no_teen_sum(a, b, c):
    return fix_teen(a) + fix_teen(b) + fix_teen(c)

#round sum
def round_sum(a, b, c):
    return round10(a) + round10(b) + round10(c)

def round10(num):
    if num % 10 >= 5:
        return num + (10 - num % 10)
    else:
        return num - (num % 10) 

#closefar
def close_far(a, b, c):
    close_b = abs(a - b) <= 1
    close_c = abs(a - c) <= 1
    far_b = abs(a - b) >= 2 and abs(b - c) >= 2
    far_c = abs(a - c) >= 2 and abs(b - c) >= 2

    return (close_b and far_c) or (close_c and far_b)

#make_chocolate
def make_chocolate(small, big, goal):
    
    max_big_bars = goal // 5
    use_big = min(big, max_big_bars)

    
    remaining = goal - (use_big * 5)

    
    if small >= remaining:
        return remaining  
    else:
        return -1  
    
#Lists2 tasks
#count_evens
def count_evens(nums):
    count = 0
    for num in nums:
        if num % 2 == 0:
            count += 1
    return count

#big_difference

def big_diff(nums):
  big = max(nums)
  small = min(nums)
  return (big - small)


#centered_average
def centered_average(nums):
    nums.remove(min(nums))   
    nums.remove(max(nums))   
    return sum(nums) // len(nums)

#sum13
def sum13(nums):
    total = 0
    skip_next = False

    for num in nums:
        if skip_next:
            skip_next = False
            continue
        elif num == 13:
            skip_next = True
            continue
        total += num

    return total

#sum67
def sum67(nums):
    total = 0
    ignore = False

    for num in nums:
        if num == 6:
            ignore = True
        elif num == 7 and ignore:
            ignore = False
        elif not ignore:
            total += num

    return total

#has22
def has22(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 2 and nums[i + 1] == 2:
            return True
    return False

