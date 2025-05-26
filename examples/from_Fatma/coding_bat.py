def sleep_in(weekday, vacation):
  if not weekday or vacation:
    return True
  else:
    return False
  
#############################################################
def monkey_trouble(a_smile, b_smile):
  if a_smile and b_smile:
    return True
  elif not a_smile and not b_smile:
    return True
  else:
    return False
  
#############################################################
def sum_double(a, b):
  sum= a + b
  if a == b:
    sum = sum * 2
    return sum
  
#############################################################

def diff21(n):
 if n <= 21:
   return 21 - n
 else:
    return (21 - n) * 2

#############################################################

def parrot_trouble(talking, hour):
 return (talking and ( hour < 7 or hour >20))

#############################################################
def makes10(a, b):
  return (a== 10 or b==10 or a+b==10)

#############################################################
def near_hundred(n): 
    return ((abs(100 - n) <= 10) or (abs(200 - n) <= 10))

#############################################################
def pos_neg(a, b, negative):
  if negative:
    return (a<0 and b<0)
  else:
    return (a>0 and b<0 or a<0 and b>0) 
  
  #############################################################
def not_string(str):
  if str[:3] =="not":
    return str
  else:
    return "not " + str
  
#############################################################
def missing_char(str, n):
  return str[:n] + str[n+1:]

#############################################################
def front_back(str):
  if len(str) <=1:
    return str
  return str[-1] + str[1:-1] + str[0]

#############################################################
def front3(str):
  return (str[:3] *3)

#############################################################
def hello_name(name):
  return "Hello " + name + "!"

#############################################################
def make_abba(a, b):
  return a+b+b+a
  
#############################################################
def make_tags(tag, word):
  return "<" +tag +">" + word + "</" +tag +">"
#############################################################
def make_out_word(out, word):
  if len(out)==4:
     return out[:2] + word + out[2:]
#############################################################
def extra_end(str):
  if len(str)>=2:
    return str[-2:] * 3
#############################################################
def first_two(str):
  if len(str)>=2:
    return str[:2]
  elif len(str)<2: 
    return str
  else:
    return " yields the empty string "
#############################################################
def first_half(str):
  return str[:len(str)//2]
#############################################################
def without_end(str):
  return str[1:-1]
#############################################################
def without_end(str):
  return str[1:-1]
#############################################################
def combo_string(a, b):
  if len(a)>len(b):
    return b+a+b
  else:
    return a+b+a
#############################################################
def non_start(a, b):
  if len(a)>=1 and len(b)>=1:
    return a[1:]+b[1:]
  else:
    return a+b
#############################################################
def left2(str):
  if len(str)>=2:
    return str[2:] + str[:2]
#############################################################
def cigar_party(cigars, is_weekend):
  if cigars>= 40 and cigars<=60:
    return True
  elif is_weekend==True and cigars>=40:
    return True
  else:
    return False
#############################################################
def date_fashion(you, date):
  if you<=2 or date<=2:
    return 0
  elif date>=8 or you>=8:
    return 2    
  else:
    return 1
#############################################################
def squirrel_play(temp, is_summer):
  if temp>=60 and temp<=90:
    return True
  elif  is_summer==True and  temp>=60 and temp<=100:
    return True
  else:
    return False
#############################################################
def caught_speeding(speed, is_birthday):
  if speed<=60:
    return 0
  elif speed>=61 and speed<=80 and is_birthday==False:
    return 1
  elif speed<=65 and is_birthday==True:
    return 0
  elif speed>=66 and speed<=85 and is_birthday==True:
    return 1
  else: 
    return 2
#############################################################
def sorta_sum(a, b):
  sum= a+b
  if sum>=10 and sum<=19 :
    return 20
  else:
    return sum
#############################################################
def alarm_clock(day, vacation):
  if  day>=1 and day<=5 and vacation==False:
    return "7:00"
  elif day>=1 and day<=5 and vacation==True:
    return "10:00"
  elif  (day==0 or day==6) and vacation==True:
    return "off"
  elif  (day==0 or day==6) and vacation==False:
    return "10:00"  
#############################################################
def love6(a, b):
  sum=a+b
  diff=abs(a-b)
  if a==6 or b==6:
    return True
  elif sum==6 or diff==6:
    return True
  else:
    return False
#############################################################
def in1to10(n, outside_mode):
  if n>=1 and n<=10 and outside_mode==False :
    return True
  elif (n<=1 or n>=10) and outside_mode==True:
    return True
  else:
    return False
#############################################################
def near_ten(num):
  num= num%10
  if num>=0 and num<=2:
    return True
  elif num==8 or num==9:
    return True
  else:
    return False
#############################################################
def double_char(str):
  result=''
  for i in str:
    result += i*2
  return result
#############################################################
def count_hi(str):
  return str.count("hi")
#############################################################
def cat_dog(str):
  return str.count('cat') == str.count('dog')
#############################################################
def count_code(str):
    count = 0
    for i in range(len(str) - 3):  
        if str[i] == 'c' and str[i+1] == 'o' and str[i+3] == 'e':
            count += 1
    return count
#############################################################
def end_other(a, b):
  a=a.lower()
  b=b.lower()
  return a.endswith(b) or b.endswith(a)
#############################################################
def xyz_there(str):
  return "xyz" in str.replace(".xyz"," ")
#############################################################
def first_last6(nums):
  return nums[0]==6 or nums[-1]==6
#############################################################
def same_first_last(nums):
  return len(nums)>=1 and nums[0] == nums[-1]
#############################################################
def make_pi():
  return [3,1,4]
#############################################################
def common_end(a, b):
  return a[0]==b[0] or a[-1]==b[-1]
#############################################################
def sum3(nums):
  return nums[0]+nums[1]+nums[2]
#############################################################
def rotate_left3(nums):
  return [nums[1],nums[2],nums[0]]
#############################################################
def reverse3(nums):
  return nums[::-1]
#############################################################
def max_end3(nums):
  larger= max(nums[0],nums[2])
  return [larger, larger,larger]
#############################################################
def sum2(nums):
  if len(nums)>=2:
    return nums[0]+nums[1]
  elif len(nums)==1:
    return nums[0]
  elif len(nums)==0:
    return 0
#############################################################
def sum2(nums):
  if len(nums)>=2:
    return nums[0]+nums[1]
  elif len(nums)==1:
    return nums[0]
  elif len(nums)==0:
    return 0
#############################################################
def make_ends(nums):
  return [nums[0],nums[-1]]
#############################################################
def has23(nums):
  if nums[0]==2 or nums[1]==2:
    return True
  elif nums[0]==3 or nums[1]==3:
    return True
  else:
    return False
#############################################################
def make_bricks(small, big, goal):
  big_bricks= min(goal//5 , big)
  remain= goal - big_bricks*5
  return remain<=smalls
#############################################################
def lone_sum(a, b, c):
  sum=a+b+c
  if a==b==c:
    return 0
  elif a==b:
    return c
  elif a==c:
    return b
  elif b==c:
    return a
  else:
    return sum
#############################################################
def lucky_sum(a, b, c):
  if a==13:
    return 0
  elif b==13:
    return a
  elif c==13:
    return a+b
  else:
    return a+b+c
#############################################################
def big_diff(nums):
  large=max(nums)
  small=min(nums)
  diff=large-small
  return diff
#############################################################
def centered_average(nums):
  sorted_nums=sorted(nums)
  centered=sorted_nums[1:-1]
  return sum(centered)//len(centered)
#############################################################
def sum13(nums):
  sum=0
  i=0
  while i<len(nums):
    if nums[i] ==13:
      i+=2
    else:
      sum+= nums[i]
      i+=1
  return sum
#############################################################
def sum67(nums):
  sum=0
  i=0
  while i<len(nums):
    if nums[i]==6:
      while nums[i]!=7:
        i+=1
      i+=1  
    else:
      sum+=nums[i]
      i+=1
  return sum    
#############################################################
def has22(nums):
  for i in range(len(nums)-1):
    if nums[i]==2 and nums[i+1]==2 :
        return True
  return False
#############################################################
def string_times(str, n):
  return str*n
#############################################################
def front_times(str, n):
  if len(str)<3:
    return str*n
  else:
    return (str[0]+str[1]+str[2])*n
#############################################################
def string_bits(str):
  return str[::2]
#############################################################
def string_splosion(str):
  result=''
  for i in range(len(str)):
    result+=str[:i+1]
  return result  
#############################################################
def last2(str):
  if len(str)<2:
    return 0
  last2= str[-2:]
  count=0
  for i in range(len(str)-2):
    if str[i:i+2]==last2:
      count+=1
  return count    
#############################################################
def array_count9(nums):
  count=0
  for num in nums:
    if num==9:
      count+=1
  return count    
#############################################################
def array_front9(nums):
  i=0
  for num in nums[:4]:
    if nums[i]==9:
      return True
    i+=1  
  return False          
#############################################################
def array123(nums):
  for i in range(len(nums)-2):
    if nums[i]==1 and nums[i+1]==2 and nums[i+2]==3:
      return True
  return False 
#############################################################
def fix_teen(n):
  if n in [13,14,17,18,19]:
    return 0
  return n

def no_teen_sum(a, b, c):
  return fix_teen(a)+fix_teen(b)+fix_teen(c)
#############################################################
def round_sum(a, b, c):
  return round10(a)+round10(b)+round10(c)
  
def round10(num):
  if num%10>=5:
    return num +(10-num%10)
  else:
    return num-(num%10)
#############################################################
def close_far(a, b, c):
  if abs(a-b)<=1 and abs(a-c)>=2 and abs(b-c)>=2:
    return True
  elif abs(a-c)<=1 and abs(a-b)>=2 and abs(b-c)>=2:
    return True
  return False  
#############################################################
def make_chocolate(small, big, goal):
  using_big=min(goal//5,big)
  remaining=goal-(using_big*5)
  if remaining<=small:
    return remaining
  else:
    return -1
#############################################################
def string_match(a, b):
  count=0
  lenght=min(len(a),len(b))
  for i in range(lenght - 1):
      if a[i:i+2]== b[i:i+2]:
         count+=1
  return count  
#############################################################
