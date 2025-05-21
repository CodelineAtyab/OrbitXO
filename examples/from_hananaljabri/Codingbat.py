#Sleep in task:
def sleep_in(weekday, vacation):
  if not weekday or vacation:
    return True
  else:
    return False
sleep_in(True,True)
###############################################################
#Monkey task :
def monkey_trouble(a_smile, b_smile):
  if a_smile == True and b_smile == True:
    return True
  elif a_smile == False and b_smile == False:
    return True
  else:
    return False
monkey_trouble(True,True)
#Monkey task another idea to write
def monkey_trouble(a_smile, b_smile):
  if (a_smile == True and b_smile == False) or (a_smile == False and b_smile == True):
    return False
  else:
    return True
monkey_trouble(True,True)
##############################################################
#Sum double task:
def sum_double(x,y):
  if x == y:
    return 2*(x+y)
  else:
    return (x+y)
sum_double(1,2)
sum_double(3,2)
sum_double(2,2)
###############################################################
#diff21 task:
def diff21(n):
  if n <= 21:
    return (21-n)
  else:
    return (n-21)*2
###############################################################
#parrot_trouble task:
def parrot_trouble(talking, hour):
  if talking and (7>hour or hour>20) :
    return True
  else:
    return False
##############################################################
#Makes10 task:
def makes10(a, b):
  if (a == 10 ) or (b == 10 ) or (a + b == 10):
    return True
  else:
    return False
##############################################################
#Near hundered task:
def near_hundred(n):
  if (90<=n<=110) or (190<=n<=210):
    return True
  else:
    return False
##############################################################
#Pos_neg task:
def pos_neg(a, b, negative):
  if (negative == False) and (((a<0) and (b>0)) or ((a>0) and (b<0))):
    return True
  elif (negative == True) and ((a<0) and (b<0)):
    return True
  else:
    return False
###############################################################
#not_string task:
def not_string(str):
  if str.startswith("not"):
    return str
  else:
    return "not " + str
################################################################
#Missing_Char:
def missing_char(text, n):
  return text[:n] + text[n+1:]
#################################################################
#string_times:
def string_times(str, n):
  result = ""
  for i in range(n):  
    result = result + str  
  return result
#################################################################
#front_times:
def front_times(str, n):
  front_len = 3
  if front_len > len(str):
    front_len = len(str)
  front = str[:front_len]
  
  result = ""
  for i in range(n):
    result = result + front
  return result
#################################################################
#string_bits:
def string_bits(str):
  result = ""
  for i in range(len(str)):
    if i % 2 == 0:
      result = result + str[i]
  return result
#################################################################
#string_splosion:
def string_splosion(str):
  result = ""
  for i in range(len(str)):
    result = result + str[:i+1]
  return result
#################################################################
#last2:
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
#################################################################
#array_count9:
def array_count9(nums):
  count = 0
  for num in nums:
    if num == 9:
      count = count + 1

  return count
#################################################################
#array_front9:
def array_front9(nums):

  end = len(nums)
  if end > 4:
    end = 4
  
  for i in range(end):  
    if nums[i] == 9:
      return True
  return False
#################################################################
#array123:
def array123(nums):
  for i in range(len(nums)-2):
    if nums[i]==1 and nums[i+1]==2 and nums[i+2]==3:
      return True
  return False
#################################################################
#string_match:
def string_match(a, b):

  shorter = min(len(a), len(b))
  count = 0
  for i in range(shorter-1):
    a_sub = a[i:i+2]
    b_sub = b[i:i+2]
    if a_sub == b_sub:
      count = count + 1

  return count
#################################################################
#Hello name Task:
def hello_name(name):
    return "Hello " + name + "!"
#################################################################
#Make abba Task:
def make_abba(a, b):
  return a+b+b+a
#################################################################
#Make tags Task:
def make_tags(tag, word):
    return "<" + tag + ">" + word + "</" + tag + ">"
#################################################################
#Make out word Task:
def make_out_word(out, word):
    return out[:2] + word + out[2:]
#################################################################
#Extra end Task:
def extra_end(str):
  result = str[-2:]
  return result*3
#################################################################
#First two Task:
def first_two(str):
  if len(str)>2:
    result = str[:2]
    return result
  else:
    return str
#################################################################
#First half Task:
def first_half(str):
  result = str[:len(str)//2]
  return result
#################################################################
#Without end Task:
def without_end(str):
  return str[1:-1]
#################################################################
#Combo string Task:
def combo_string(a, b):
  if (len(a) > len(b)):
    return b+a+b
  else:
    return a+b+a
#################################################################
#non start:
def non_start(a, b):
    return a[1:] + b[1:]
#################################################################
#Left2:
def left2(text):
    return text[2:] + text[:2]
#################################################################
#List1
#First last 6:
def first_last6(nums):
  if nums[0]==6 or nums[-1]==6:
    return True
  else:
    return False
#################################################################
#Same first last:
def same_first_last(nums):
  if (len(nums)>=1) and (nums[0]== nums[-1]):
    return True
  else:
    return False
#################################################################
#Make pi:
def make_pi():
  return [3,1,4]
#################################################################
#Commen end:
def common_end(a, b):
  if ((len(a)>=1) and (len(b)>=1)) and ((a[0]==b[0]) or (a[-1]==b[-1])):
    return True
  else:
    return False
#################################################################
#Sum3:
def sum3(nums):
  sum = nums[0] + nums[1] + nums[2]
  return sum
#################################################################
#rotate left3:
def rotate_left3(nums):
  return [nums[1], nums[2], nums[0]]
#################################################################
#reverse3:
def reverse3(nums):
  return nums[::-1]
#################################################################
#Max end3:
def max_end3(nums):
  if nums[0]>nums[2]:
    return [nums[0],nums[0],nums[0]]
  else:
    return [nums[2],nums[2],nums[2]]
#################################################################
#sum2:
def sum2(nums):
    if len(nums) >= 2:
        return nums[0] + nums[1]
    elif len(nums) == 1:
        return nums[0]
    else:
        return 0
#################################################################
#middle way:
def middle_way(a, b):
  if (len(a)>1 and len(b)>1):
    return [a[1],b[1]]
#################################################################
#make ends:
def make_ends(nums):
  if len(nums)>=1 :
    return [nums[0],nums[-1]]
#################################################################
#has23:
def has23(nums):
  if (2 in nums) or (3 in nums) :
    return True
  else:
    return False
#################################################################
#Logic-1
#cigar_party:
def cigar_party(cigars, is_weekend):
    if is_weekend:
        return cigars >= 40
    else:
        return 40 <= cigars <= 60
#################################################################
#date_fashion
def date_fashion(you, date):
    if you <= 2 or date <= 2:
        return 0
    elif you >= 8 or date >= 8:
        return 2
    else:
        return 1
#################################################################
#squirrel_play
def squirrel_play(temp, is_summer):
    upper_limit = 100 if is_summer else 90
    return 60 <= temp <= upper_limit
#################################################################
#caught_speeding
def caught_speeding(speed, is_birthday):
    allowance = 5 if is_birthday else 0
    speed_adjusted = speed - allowance

    if speed_adjusted <= 60:
        return 0
    elif speed_adjusted <= 80:
        return 1
    else:
        return 2
#################################################################
#sorta_sum
def sorta_sum(a, b):
    total = a + b
    if 10 <= total <= 19:
        return 20
    else:
        return total
#################################################################
#alarm_clock
def alarm_clock(day, vacation):
    is_weekend = (day == 0 or day == 6)
    
    if vacation:
        if is_weekend:
            return "off"
        else:
            return "10:00"
    else:
        if is_weekend:
            return "10:00"
        else:
            return "7:00"
#################################################################
#love6:
def love6(a, b):
    return (a == 6 or b == 6 or (a + b) == 6 or abs(a - b) == 6)
#################################################################
#in1to10
def in1to10(n, outside_mode):
    if outside_mode:
        return n <= 1 or n >= 10
    else:
        return 1 <= n <= 10
#################################################################
#near_tan:
def near_ten(num):
    remainder = num % 10
    return remainder <= 2 or remainder >= 8
#################################################################
#logic2:
#make_bricks:
def make_bricks(small, big, goal):
    max_big_bricks = goal // 5
    big_bricks_used = min(big, max_big_bricks)
    remaining = goal - big_bricks_used * 5
    return small >= remaining
#################################################################
#Lone_sum
def lone_sum(a, b, c):
    if a == b == c:
        return 0
    elif a == b:
        return c
    elif a == c:
        return b
    elif b == c:
        return a
    else:
        return a + b + c
#################################################################
#lucky_sum:
def lucky_sum(a, b, c):
    if a == 13:
        return 0
    elif b == 13:
        return a
    elif c == 13:
        return a + b
    else:
        return a + b + c
#################################################################
#no_teen_sum
def fix_teen(n):
    if 13 <= n <= 19 and n not in (15, 16):
        return 0
    return n

def no_teen_sum(a, b, c):
    return fix_teen(a) + fix_teen(b) + fix_teen(c)
#################################################################
#round_sum
def round_sum(a, b, c):
    return round10(a) + round10(b) + round10(c)

def round10(num):
    if num % 10 >= 5:
        return num + (10 - num % 10)
    else:
        return num - (num % 10)
#################################################################
#close_far
def close_far(a, b, c):
    close = abs(a - b) <= 1 or abs(a - c) <= 1
    far_b = abs(a - b) >= 2 and abs(b - c) >= 2
    far_c = abs(a - c) >= 2 and abs(c - b) >= 2

    return (abs(a - b) <= 1 and far_c) or (abs(a - c) <= 1 and far_b)
#################################################################
# make_chocolate
def make_chocolate(small, big, goal):
    max_big = min(goal // 5, big)  # Use as many big bars as possible, but not more than needed
    remaining = goal - (max_big * 5)
    
    if remaining <= small:
        return remaining  # Number of small bars needed
    else:
        return -1 
#################################################################
#sring2:
#Double char Task:
def double_char(str):
    result = ""
    for letter in str:
        result = result + letter + letter
    return result
################################################################
#Count hi Task:
def count_hi(str):
  return str.count("hi")
################################################################
#Cat dog Task:
def cat_dog(str):
  cat = str.count("cat")
  dog = str.count("dog")
  if cat == dog:
    return True
  else:
    return False
################################################################
#Count code Task:
def count_code(text):
    count = 0
    i = 0
    while i < len(text) - 3:
        word = text[i:i+4]
        if word[0] == "c" and word[1] == "o" and word[3] == "e":
            count = count + 1
        i = i + 1
    return count
################################################################
#End other Task:
def end_other(a, b):
  a = a.lower()
  b = b.lower()
  if a.endswith(b) or b.endswith(a):
    return True
  else:
    return False
################################################################
#XYZ there Task:
def xyz_there(str):
  if ".xyz" in str:
    return "xyz" in str.replace(".xyz", "")
  else:
    return "xyz" in str
################################################################
#LIST 2
#Count evens Task:
def count_evens(nums):
    count = 0
    for number in nums:
        if number % 2 == 0:
            count = count + 1
    return count
################################################################
#Big diff Task:
def big_diff(nums):
  maxi = max(nums)
  mini = min(nums)
  substract = maxi - mini
  return substract
################################################################
#Centered average Task:
def centered_average(nums):
  nums.remove(max(nums))
  nums.remove(min(nums))
  return sum(nums) // len(nums)
################################################################
#Sum13 Task:
def sum13 (nums):
  total = 0
  i = 0
  while i < len(nums):
    if nums[i] == 13:
      i = i + 2 #skip 2 numbers
    else:
      total = total + nums[i]
      i = i + 1
  return total
################################################################
#Sum67 Task:
def sum67(nums):
    total = 0
    skip = False
    for number in nums:
        if number == 6:
            skip = True
        elif skip and number == 7:
            skip = False
        elif not skip:
            total += number
    return total
################################################################
#Hass22 Task:
def has22(nums):
    i = 0
    while i < len(nums) - 1:
        if nums[i] == 2 and nums[i + 1] == 2:
            return True
        i = i + 1
    return False

#################################################################
