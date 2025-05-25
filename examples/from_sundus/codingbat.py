
#=========CodingBat============

#Warmup-1  

# sleep_in
def sleep_in(weekday, vacation):
  if not weekday or vacation:
    return True 
  else: 
    return False

######################

#sum_double
def sum_double(a, b):
  if a == b: 
    return (( a + b ) * 2) 
    
  else: 
    return ( a + b ) 
  
######################


#Warmup-2

#string_times
def string_times(str, n):
  return str * n 

##################

#string_bits

def string_bits(str):
  return str [::2]

######################

#String-1 

#hello_name

def hello_name(name):
  return "Hello " + name + "!"

#################

#make_tags
def make_tags(tag, word):
  return "<" + tag + ">" + word + "</" + tag + ">"

################
     
#List-1 

#first_last6

def first_last6(nums):
  return nums[0] == 6 or nums[-1] == 6

###################

#make_pi 
def make_pi():
  return [3,1,4]

##################

#Logic-1 

#alarm_clock
def alarm_clock(day, vacation):
  if vacation: 
    if day == 0 or day == 6: 
      return 'off'
    else: 
      return '10:00'
      
  else: 
    if day == 0 or day == 6: 
      return '10:00' 
    else: 
      return '7:00'
    
###############################   

#in1to10

def in1to10(n, outside_mode):
  if outside_mode: 
    
   return 1 >= n or n >= 10 
       
  else : 
    return 1 <= n <= 10
  
############################## 


#Logic-2 

#lone_sum

def lone_sum(a, b, c):
  sum = 0
  
  if a != b and a != c:
      sum += a
  if b != a and b != c:
       sum += b
  if c != a and c != b:
      sum += c
  return sum

#######################

#round_sum

def round_sum(a, b, c):
    return round10(a) + round10(b) + round10(c)

def round10(num):
    if num % 10 >= 5:
        return ((num // 10) + 1) * 10
    else:
        return (num // 10) * 10
    
######################



#String-2

#double_char

def double_char(str):
 
  result = ""
  
  for char in str:
    result += char * 2
    
  return result   

#########################


#count_hi

def count_hi(str):
    return str.count("hi")

#########################


#List-2

#big_diff

def big_diff(nums):
  v1= min(nums)
  v2= max(nums) 
    
  return v2 - v1

#####################

#has22

def has22(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 2 and nums[i + 1] == 2:
            return True
    return False

##########################