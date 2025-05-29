############ WARMUP 1 ################

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

#Front back task:
def front_back(str):
  if len(str) <= 1:
    return str  
  else:
    first = str[0]
    last = str[-1]
    middle = str[1:-1]
    return last + middle + first

#################################################################

#front3 task:
def front3(str):
  check = str[:3]
  return check*3

##################################################################

############ WARMUP 2 ################

#string_times task:
def string_times(str, n):
  return str*n

##################################################################

#Front times task:
def front_times(str, n):
  front = str[:3]
  return front*n

##################################################################

#String_bits task:
def string_bits(str):
  return str[::2]

##################################################################

#String_spolsion task:
def string_splosion(str):
  result = ""
  for i in range(1, len(str) + 1):
    result = result + str[:i]
  return result

##################################################################

#Last2 task:
def last2(str):
  target = str[-2:]         
  count = 0
  for i in range(len(str) - 2):  
    if str[i:i+2] == target:
      count += 1
  return count

##################################################################

#Array count 9 task:
def array_count9(nums):
  return nums.count(9)

##################################################################

#Array front 9 Task:
def array_front9(nums):
  if 9 in nums[:4]:
    return True
  else:
    return False
  
##################################################################

#Array 123 Task:
def array123(nums):
    for i in range(len(nums) - 2):  
        if nums[i] == 1 and nums[i+1] == 2 and nums[i+2] == 3:
            return True
    return False

##################################################################

#String match Task:
def string_match(a, b):
    count = 0
    length = min(len(a), len(b))  # shortest length of the two strings

    for i in range(length - 1):  # loop until 2-letter substrings can be compared
        if a[i:i+2] == b[i:i+2]:
            count += 1

    return count

################################################################

############ STRING 1 ################
#Hello name Task:
def hello_name(name):
    return "Hello " + name + "!"
################################################################
#Make abba Task:
def make_abba(a, b):
  return a+b+b+a
################################################################
#Make tags Task:
def make_tags(tag, word):
    return "<" + tag + ">" + word + "</" + tag + ">"
################################################################
#Make out word Task:
def make_out_word(out, word):
    return out[:2] + word + out[2:]
################################################################
#Extra end Task:
def extra_end(str):
  result = str[-2:]
  return result*3
################################################################
#First two Task:
def first_two(str):
  if len(str)>2:
    result = str[:2]
    return result
  else:
    return str
################################################################
#First half Task:
def first_half(str):
  result = str[:len(str)//2]
  return result
################################################################
#Without end Task:
def without_end(str):
  return str[1:-1]
################################################################
#Combo string Task:
def combo_string(a, b):
  if (len(a) > len(b)):
    return b+a+b
  else:
    return a+b+a
################################################################
#non start Task:
def non_start(a, b):
    return a[1:] + b[1:]
################################################################
#Left2 Task:
def left2(text):
    return text[2:] + text[:2]

############ LIST 1 ################
#First last 6 Task:
def first_last6(nums):
  if nums[0]==6 or nums[-1]==6:
    return True
  else:
    return False
################################################################
#Same first last Task:
def same_first_last(nums):
  if (len(nums)>=1) and (nums[0]== nums[-1]):
    return True
  else:
    return False
################################################################
#Make pi Task:
def make_pi():
  return [3,1,4]
################################################################

#Commen end Task:
def common_end(a, b):
  if ((len(a)>=1) and (len(b)>=1)) and ((a[0]==b[0]) or (a[-1]==b[-1])):
    return True
  else:
    return False
################################################################
#Sum3 Task:
def sum3(nums):
  sum = nums[0] + nums[1] + nums[2]
  return sum
################################################################
#rotate left3 Task:
def rotate_left3(nums):
  return [nums[1], nums[2], nums[0]]
################################################################
#reverse3 Task:
def reverse3(nums):
  return nums[::-1]
################################################################
#Max end3 Task:
def max_end3(nums):
  if nums[0]>nums[2]:
    return [nums[0],nums[0],nums[0]]
  else:
    return [nums[2],nums[2],nums[2]]
################################################################
#sum2 Task:
def sum2(nums):
    if len(nums) >= 2:
        return nums[0] + nums[1]
    elif len(nums) == 1:
        return nums[0]
    else:
        return 0
################################################################
#middle way Task:
def middle_way(a, b):
  if (len(a)>1 and len(b)>1):
    return [a[1],b[1]]
################################################################
#make ends Task:
def make_ends(nums):
  if len(nums)>=1 :
    return [nums[0],nums[-1]]
################################################################
#has23 Task:
def has23(nums):
  if (2 in nums) or (3 in nums) :
    return True
  else:
    return False
################################################################

############ LOGIC 1 ################
#Cigar party Task:
def cigar_party(cigars, is_weekend):
  if 40<=cigars<=60 and not is_weekend:
    return True
  elif 40<=cigars and is_weekend:
    return True
  else:
    return False
################################################################
#date fashion Task:
def date_fashion(you, date):
  if you<=2 or date<=2:
    return 0
  elif you>=8 or date>=8:
    return 2
  else:
    return 1
################################################################
#squirrel play Task:
def squirrel_play(temp, is_summer):
  if 60<=temp<=90 and not is_summer:
    return True
  elif 60<=temp<=100 and is_summer:
    return True
  else:
    return False
################################################################
#Caught speeding Task:
def caught_speeding(speed, is_birthday):
    if is_birthday:
        speed = speed - 5  
    if speed <= 60:
        return 0  
    elif speed <= 80:
        return 1 
    else:
        return 2 
################################################################
#sorta sum Task:
def sorta_sum(a, b):
  sum = a + b
  if 10<=sum<=19:
    return 20
  else:
    return sum
################################################################
#alarm clock Task:
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
################################################################
#Love6 Task:
def love6(a, b):
  if (a == 6) or (b == 6) or ((a+b)==6) or (abs(a-b)==6):
    return True
  else:
    return False
################################################################
#In 1 to 10 Task:
def in1to10(n, outside_mode):
    if outside_mode:
        return n <= 1 or n >= 10
    else:
        return 1 <= n <= 10
################################################################
#Near ten Task:
def near_ten(num):
    return num % 10 <= 2 or num % 10 >= 8
################################################################
#make bricks Task:
def make_bricks(small, big, goal):
  big_bricks_we_can_use = min(big, goal // 5)
  remaining_inches = goal - (big_bricks_we_can_use * 5)
  if small >= remaining_inches:
    return True
  else:
    return False
################################################################
#Lone sum Task:
def lone_sum(a, b, c):
    if a == b and b == c:
        return 0  
    elif a == b:
        return c  
    elif a == c:
        return b  
    elif b == c:
        return a  
    else:
        return a + b + c  
################################################################
#Lucky sum Task:
def lucky_sum(a, b, c):
    if a == 13:
        return 0
    elif b == 13:
        return a
    elif c == 13:
        return a + b
    else:
        return a + b + c
################################################################
#No teen sum Task:
def no_teen_sum(a, b, c):
    return fix_teen(a) + fix_teen(b) + fix_teen(c)
def fix_teen(n):
    if n in [13, 14, 17, 18, 19]:
        return 0
    else:
        return n
################################################################
#Round sum Task:
def round_sum(a, b, c):
    return round10(a) + round10(b) + round10(c)

def round10(num):
    last_digit = num % 10
    if last_digit >= 5:
        return num + (10 - last_digit)
    else:
        return num - last_digit
################################################################
#Close far Task:
def close_far(a, b, c):
    if abs(a - b) <= 1 and abs(a - c) >= 2 and abs(b - c) >= 2:
        return True
    if abs(a - c) <= 1 and abs(a - b) >= 2 and abs(b - c) >= 2:
        return True
    return False
################################################################
#Make chocolate Task:
def make_chocolate(small, big, goal):
    big_used = min(big, goal // 5)
    remaining = goal - (big_used * 5)
    
    if small >= remaining:
        return remaining
    else:
        return -1
################################################################

############ STING 2 ################
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

############ LIST 2 ################
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
################################################################
