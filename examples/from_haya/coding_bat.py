"""bat pract for python"""
#######################################################################################
"""warm up -1"""
#######################################################################################
#sleep_in 
def sleep_in(weekday,vication):
    if not weekday or vication:     #not will sprate for the two vairable
        return True
    else:
        return False

sleep=sleep_in(False,True)
print( sleep ) 

#monkey_trouble
def monkey_trouble(a_smile, b_smile):
  if a_smile and b_smile:
    return True
  if not a_smile and not b_smile:      
    return True
  else:
    return False
     
monkey=monkey_trouble(True,True)
print(monkey)

#sum double
def sum_double(a, b):
  if a != b:
    sum=a+b
    return sum
  if a==b :
    x=(a+b)*2
    return x

num=sum_double(2,2)
print(num)

#diff21
def diff21(n):
  if n<=21:
    return abs(n - 21)
  else:
    return abs((n-21)*2)
  
x=diff21(50)
print(x)

#parrot_trouble
def parrot_trouble(talking, hour):
  return (talking and (hour<7 or hour>20))
     
D=parrot_trouble(True,8)
print(D)

#make10
def makes10(a, b):
  return ((a==10 or b==10) or (a+b==10))

P=makes10(2,5)
print(P)

#near_hundred
def near_hundred(n):
  return (n >= 90 and n <= 110) or (n >= 190 and n <= 210)

c=near_hundred(110)
print(c)

# pos_neg
def pos_neg(a, b, negative):
  if (a<0 and b<0 ) and negative == True:
   return True
  elif ((a<0 and b>0) or(a>0 and b<0)) and negative == False:
    return True
  else:
    return False

f=pos_neg(1,1,True)
print(f)

#not_string
def not_string(str):
  if str[0:4] == "not ":
    return str
  elif str=="not":
    return str
  else:
    return "not " + str

h=not_string("not haya")
print(h)

#missing_char
def missing_char(str, n):
  return str[0:n] + str[n+1:] #first print str from 0 tell n(letter position) add n+1 position tell end

ll=missing_char("haya",2)
print(ll)

#front back
def front_back(str):
  return str[-1] + str[1:-1] + str[0]

yy=front_back("ghadeer")
print(yy)

#front3
def front3(str):
  if len(str) >= 3:
    return str[0:3]+str[0:3]+str[0:3]
  if len(str) <= 2:
    return str[0:2]+str[0:2]+str[0:2]
  else:
    return str
  
  
gg=front3("ab")
print(gg)
#########################################################################################
"""warm up -2"""
#########################################################################################
#string_times
def string_times(str, n):
  return (str *n )

dd=string_times("haya",2)
print(dd)

#front_times
def front_times(str, n):
  return (str[0:3] * n) 

tt=front_times("haya",3)
print(tt)

#string bits 
def string_bits(str):
    result = ""
    for i in range(len(str)):
        if i % 2 == 0:
            result += str[i]
    return result

st=string_bits("python")
print(st)

#string_splosio
def string_splosion(str):
  result = ""
  for i in range(len(str)):
    result = result + str[:i+1]
  return result

ss=string_splosion("haya")
print(ss)

#last2
def last2(str):
  last2 =str[-2:] 
  count = 0
  for i in range(len(str)-2):
    sub = str[i:i+2]
    if sub == last2:
      count = count + 1
  return count

last=last2("shdhkkudhsukk")
print(last)

#array count9
def array_count9(nums):
    count = 0 #start count from zero
    for num in nums: 
        if num == 9:
            count += 1 #check first 0 position + 1 position + 2 position 
    return count

array=array_count9([1,9,9,9]) 
print(array)

#array_front9
def array_front9(nums):
    last = min(4, len(nums))
    for i in range(last):
        if nums[i] == 9:
            return True
    return False

kl=array_front9([2,3,9,3])
print(kl)

#array123
def array123(nums):
  for i in range(len(nums) - 2):
    if nums[i] == 1 and nums[i+1] == 2 and nums[i+2] == 3:
      return True
  return False

ar123=array123([1,2,3.8,1,2,3])
print(ar123)

#string match
def string_match(a, b):
  count = 0
  shorter_length = min(len(a), len(b)) 
  for i in range(shorter_length - 1):
    if a[i:i+2] == b[i:i+2]:
       count += 1 
  return count

ff=string_match("haya","python ")
print(ff)
#########################################################################################
"""String - 1"""
#########################################################################################
#hello_name
def hello_name(name):
  return "Hello" +" "+ name + "!"

#make_abba
def make_abba(a, b):
  return a + b + b + a

#make_tags
def make_tags(tag, word):
  return "<" +tag+ ">" + word +  "</" + tag + ">" 

#make_out_word
def make_out_word(out, word):
  return out[0:2] + word + out[2:]

# extra_end
def extra_end(str):
  return str[-2:] *3 

#first_two
def first_two(str):
  return str[0:2]

#first_half
def first_half(str):
  result=len(str)/2
  return str[0:result]

#without_end
def without_end(str):
  return str[1:-1]

#combo_string
def combo_string(a, b):
  if len(a) > len(b):
    return b + a + b
  if len(a) < len(b):
    return a + b +a

#non_start
def non_start(a, b):
  return a[1:] + b[1:]

#left2
def left2(str):
  if len(str)>2:
    return str[2:] + str[:2]
  else:
    return str
#######################################################################################
"""Logic -1 """
#######################################################################################
#cigar_party
def cigar_party(cigars, is_weekend):
  if (40<= cigars >= 60) and is_weekend == True :
    return True
  if (cigars >= 40) and is_weekend == True :
    return True
  if (cigars > 60) and is_weekend == False :
    return False
  if (cigars >= 40) and is_weekend == False :
     return True
  else:
    return False

#date_fashion
def date_fashion(you, date):
  if (you <= 2) or (date <= 2):
    return 0
  if (you >= 8) or (date >= 8):
    return 2
  if (3 <= you <= 7) and (3 <= date <= 7):
    return 1
  else:
    return 1

#squirrel_play
def squirrel_play(temp, is_summer):
  if 60 <= temp <= 100 and is_summer:
    return True 
  else:
    return 60 <= temp <= 90

#aught_speeding
def caught_speeding(speed, is_birthday):
  if is_birthday == False:
    if speed <= 60:
      return 0
    elif 61 <= speed <= 80:
      return 1
    else:  
      return 2
  else: 
    if speed <= 65:
      return 0
    elif 66 <= speed <= 85:
      return 1
    else: 
      return 2

#sorta_sum
def sorta_sum(a, b):
  result=a+b
  if 10 <= result <=19:
    return 20
  else:
    return result

#alarm_clock
def alarm_clock(day, vacation):
  if vacation == False:
    if 1 <= day <= 5:
      return "7:00"
    else:  
      return "10:00"
  else: 
    if 1 <= day <= 5:
      return "10:00"
    else: 
      return "off"

#love6
def love6(a, b):
  result_sum=a+b
  result_sub=abs(a-b)
  if a == 6 or b == 6:
    return True
  elif result_sum == 6 or result_sub ==6:
    return True 
  else:
    return False

#in1to10
def in1to10(n, outside_mode):
  if n<=10 and n>=1 and outside_mode== False:
    return True
  elif (n>=10 or n<=1) and outside_mode== True :
    return True
  else:
    return False

#near_ten    
def near_ten(num):
  remainder = num % 10
  return remainder <= 2 or remainder >= 8
###################################################################################
"""String - 2"""
###################################################################################
#double_char
def double_char(str):
  result = ''
  for char in str:
    result += char * 2
  return result

# count_hi
def count_hi(str):
  return str.count("hi")

#cat_dog
def cat_dog(str):
   return str.count('cat') == str.count('dog')

#count_code
def count_code(str):
    count = 0
    for c in range(len(str) - 3):
        if str[c:c+2] == 'co' and str[c+3] == 'e':
            count += 1
    return count

#end_other
def end_other(a, b):
  a= a.lower()
  b= b.lower()
  len_a = len(a)
  len_b = len(b)
  if a[len_a - len_b:] == b:
    return True
  if b[len_b - len_a:] == a:
    return True
  return False

#xyz_there
def xyz_there(str):
    for i in range(len(str) - 2):
        if str[i:i+3] == 'xyz':     #from 0 to 3 position = xyz
            if i == 0 or str[i-1] != '.':  
                return True
    return False
######################################################################################
"""List - 1"""
######################################################################################
#first_last6
def first_last6(nums):
    return nums[0]==6 or nums[-1]==6

#same_first_last
def same_first_last(nums):
  return ((len(nums) >= 1)and(nums[0]==nums[-1]))

# make_pi
def make_pi():
  return [3,1,4]

# common_end
def common_end(a, b):
  return (len(b)>=1 and len(a)) and((a[0]==b[0])or a[-1]==b[-1])
                                    
#sum3
def sum3(nums):
  return nums[0]+nums[1]+nums[2]

#rotate_left3
def rotate_left3(nums):
 return [nums[1],nums[2],nums[0]]

#reverse3
def reverse3(nums):
  return nums[::-1]

#max_end3
def max_end3(nums):
  if nums[0]>nums[-1]:
    return [nums[0],nums[0],nums[0]]
  if nums[0]<nums[-1]:
    return [nums[-1],nums[-1],nums[-1]]
  else:
    return [nums[-1],nums[-1],nums[-1]]

#sum2
def sum2(nums):
  if len(nums) >= 2:
    return nums[0] + nums[1]
  elif len(nums) == 1:
    return nums[0]
  else:
    return 0

# middle_way
def middle_way(a, b):
  return [a[1],b[1]]

#make_ends
def make_ends(nums):
  return [nums[0],nums[-1]]

#has23
def has23(nums):
  if nums[0]==2 or nums[1]==3:
    return True
  elif nums[0]==3 or nums[1]==2:
     return True
  else:
    return False
#######################################################################################
"""Logic - 2 """
#######################################################################################
#make_bricks
def make_bricks(small, big, goal):
  big_length = big * 5
  total_length = small + big_length
  if total_length < goal:
    return False
  if (goal % 5) <= small:
    return True
  else:
    return False
  
#lone_sum
def lone_sum(a, b, c):
  if a==b==c:
    return 0
  elif a==b :
    return c
  elif a==c:
    return b
  elif c==b:
    return a
  elif a!=b and a!=c:
    return a+b+c
  elif a==b==c:
    return 0
  else:
    return

#lucky_sum
def lucky_sum(a, b, c):
  if a==13:
    return 0
  elif b==13:
    return a
  elif c==13:
    return a+b
  elif a!=13 and b!=13 and c!=13:
    return a+b+c
  else:
    return
  
#no_teen_sum
def no_teen_sum(a, b, c):
  if a == 13 or a == 14 or a == 17 or a == 18 or a == 19:
    a = 0
  if b == 13 or b == 14 or b == 17 or b == 18 or b == 19:
    b = 0
  if c == 13 or c == 14 or c == 17 or c == 18 or c == 19:
    c = 0
  total = a + b + c
  return total
 
#round_sum
def round_sum(a, b, c):
  if a % 10 >= 5:
    a = a + (10 - (a % 10))
  else:
    a = a - (a % 10)

  if b % 10 >= 5:
    b = b + (10 - (b % 10))
  else:
    b = b - (b % 10)

  if c % 10 >= 5:
    c = c + (10 - (c % 10))
  else:
    c = c - (c % 10)

  total = a + b + c
  return total

#make_chocolate
def make_chocolate(small, big, goal):
  big_needed = goal / 5

  if big_needed <= big:
    goal = goal - (big_needed * 5)
  else:
    goal = goal - (big * 5)

  if goal <= small:
    return goal
  else:
    return -1
########################################################################################
"""List - 2"""
########################################################################################
#count_evens
def count_evens(nums):
  count = 0
  for n in nums:
    if n % 2 == 0:
      count = count + 1
  return count

#big_diff
def big_diff(nums):
  big = max(nums)
  small = min(nums)
  result = big - small
  return result

#centered_average
def centered_average(nums):
  nums.remove(max(nums))
  nums.remove(min(nums))
  total = sum(nums)
  average = total / len(nums)
  return average

#sum13
def sum13(nums):
  total = 0
  X = 0
  while X < len(nums):
    if nums[X] == 13:
      X = X + 2
    else:
      total = total + nums[X]
      X = X+ 1
  return total

#sum67
def sum67(nums):
  total = 0
  in_section = False
  for n in nums:
    if n == 6:
      in_section = True
    elif n == 7 and in_section:
      in_section = False
    elif not in_section:
      total = total + n
  return total

#has22
def has22(nums):
  for i in range(len(nums) - 1):
    if nums[i] == 2 and nums[i+1] == 2:
      return True
  return False
##########################################################################
"""the end of coding bat"""
##########################################################################