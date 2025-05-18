##############################

# WARMUP-1

###############################
#Double Sum : 
def sum_double(x, y):

    if x == y : #int are the same
        return 2*(x + y)
    else:
        return x + y #int are different 
 # Test cases
print(sum_double(1, 2))  # Output: 3
print(sum_double(3, 2))  # Output: 5
print(sum_double(2, 2))  # Output: 8

#################################
# Monkey Trouble:
#code block 
def monkey_trouble (a_smile, b_smile):

    if (a_smile==True and b_smile==True):
      return True 
    elif(a_smile==False and b_smile==False):
      return True 

    else :
     return False 
    # output of the function
    print(monkey_trouble (True, True))
    print(monkey_trouble (False, False))
    print(monkey_trouble (False, True))

#######################################

#sleep in :
def sleep_in(weekday, vacation):
  if not weekday or vacation:
    return True
  else:
    return False
  
print(sleep_in(False, False))#True
print(sleep_in(True, False)) #False
print(sleep_in(False, True)) #True solve

#######################################

#diff21 :
def diff21(n):
    if n > 21:
        return 2 * (n - 21)
    else:
        return 21 - n

######################################
#Parrot_trouble :
def parrot_trouble(talking, hour):
    return talking and (hour < 7 or hour > 20)

##########################################

#Makes 10  :
def makes10(a, b):
    return a == 10 or b == 10 or (a + b) == 10

##############################################

#def hundred :
def near_hundred(n):
    return abs(100 - n) <= 10 or abs(200 - n) <= 10

############################################
#pos_neg :
def pos_neg(a, b, negative):
    if negative:
        return a < 0 and b < 0
    else:
        return (a < 0 and b > 0) or (a > 0 and b < 0)
#################################

    #not string :
def not_string(s): 
    if s.startswith("not"):
        return s
    else:
        return "not " + s
    
 ##########################################
    
    #Missing char :
def missing_char(s, n):
    return s[:n] + s[n+1:]
 
 ##########################################

 # front and back :
def front_back(s):
    if len(s) <= 1:
        return s
    return s[-1] + s[1:-1] + s[0]

############################################

#front3 :
def front3(s):
    return s[:3] * 3
############################################

#WARMUP-2 

############################################

#string times :
def string_times(s, n):
    return s * n

#############################################

#front times :
def front_times(s, n):
    front = s[:3] 
    return front * n  
###############################################

#string bits :
def string_bits(s):
    return s[::2]

#############################################

#string splosion :
def string_splosion(s):
    return ''.join(s[:i+1] for i in range(len(s)))

##############################################

#last2 :
def last2(s):
  
    last_two = s[-2:]
    
  
    count = 0
    
  
    for i in range(len(s) - 2):
        if s[i:i+2] == last_two:
            count += 1
    
    return count

#######################################

#array_count9 :

def array_count9(nums):
    return nums.count(9)

########################################

#array front9 :
def array_front9(nums):
  
    return 9 in nums[:4]

######################################

#array123 :
def array123(nums):
    for i in range(len(nums) - 2):
        if nums[i:i+3] == [1, 2, 3]:
            return True
    return False

#########################################

#string_match :
def string_match(a, b):
    count = 0
    
    for i in range(min(len(a), len(b)) - 1):
        if a[i:i+2] == b[i:i+2]:
            count += 1
    
    return count

########################################
#hello name :
def hello_name(name):
    return f"Hello {name}!"

###################################

#String -1

###################################

# hello name :
def hello_name(name):
    return "Hello " + name + "!"

###################################

#make abba :
def make_abba(a, b):
    return a + b + b + a

###############################

#make tags :
def make_tags(tag, word):
    return "<" + tag + ">" + word + "</" + tag + ">"


######################################

#make out word :
def make_out_word(out, word):
    return out[:2] + word + out[2:]

################################
#extra end :
def extra_end(s):
    return s[-2:] * 3

#################################
#first two: 
def first_two(s):
    return s[:2]

###############################
#first half :
def first_half(s):
    return s[:len(s) // 2]
 ################################

 #without end 
def without_end(s):
    return s[1:-1]

#################################
#combo string :
def combo_string(a, b):
    if len(a) < len(b):
        return a + b + a
    else:
        return b + a + b
    
 #################################
# nom start :
def non_start(a, b):
    return a[1:] + b[1:]
 
 ##################################
 #left2 :
def left2(s):
    return s[2:] + s[:2]
######################################

#first_last6 :
def first_last6(nums):
    return nums[0] == 6 or nums[-1] == 6

##########################################
#same first last:
def same_first_last(nums):
    return len(nums) >= 1 and nums[0] == nums[-1]
#############################################

#Make pi :
def make_pi():
    return [3, 1, 4]
###############################################
#common end :
def common_end(a, b):
    return a[0] == b[0] or a[-1] == b[-1]
###############################################
#sum 3 :
def sum3(nums):
    return sum(nums)
###############################################

#rotate left 3 : 
def rotate_left3(nums):
    return [nums[1], nums[2], nums[0]]
################################################

#reverse 3: 
def reverse3(nums):
    return nums[::-1]
###############################################
#max end :
def max_end3(nums):
    if nums[0] > nums[2]:
        max_val = nums[0]
    else:
        max_val = nums[2]
    return [max_val, max_val, max_val]
#################################################
#sum2 :
def sum2(nums):
    if len(nums) >= 2:
        return nums[0] + nums[1]
    elif len(nums) == 1:
        return nums[0]
    else:
        return 0
################################################
#middle way : 
def middle_way(a, b):
    return [a[1], b[1]]
################################################
#make end :
def make_ends(nums):
    return [nums[0], nums[-1]]
################################################
#has 23 :
def has23(nums):
    return 2 in nums or 3 in nums
####################################################

#LOGIC- 1

####################################################

#Date fashion : 
def date_fashion(you, date):
    if you <= 2 or date <= 2:
        return 0
    elif you >= 8 or date >= 8:
        return 2
    else:
        return 1

#####################################################
#cigar party :
def cigar_party(cigars, is_weekend):
    if is_weekend:
        return cigars >= 40
    else:
        return 40 <= cigars <= 60

###################################################
#squirrel_play :
def squirrel_play(temperature, is_summer):
    if is_summer:
        return 60 <= temperature <= 100
    else:
        return 60 <= temperature <= 90
    
##################################################
#caught speeding :
def caught_speeding(speed, is_birthday):
  
    if is_birthday:
        speed -= 5 # if its your birthday !

    if speed <= 60:
        return 0
    elif speed <= 80:
        return 1
    else:
        return 2
    #################################################
#sotra sum :
def sorta_sum(a, b):
    total = a + b
    if 10 <= total <= 19:
        return 20
    else:
        return total
######################################################
#alarm clock : 
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
######################################################
#love6:
def love6(a, b):
    return a == 6 or b == 6 or a + b == 6 or abs(a - b) == 6

########################################################

#into10:
def in1to10(n, outside_mode):
    if outside_mode:
        return n <= 1 or n >= 10
    else:
        return 1 <= n <= 10
    
###################################################
#near ten:
def near_ten(num):
    return num % 10 <= 2 or num % 10 >= 8

####################################################

#STRING-2

#####################################################
#double char :
def double_char(s):
    result = ""
    for char in s:
        result += char * 2
    return result
#########################################################
#count Hi :
def count_hi(s):
    return s.count('hi')
###########################################################
#cat and dog :
def cat_dog(s):
    if s.count('cat') == s.count('dog'):
        return True
    else:
        return False

#########################################################
#count code:
def count_code(s):
    count = 0
    for i in range(len(s) - 3): 
        if s[i:i+2] == "co" and s[i+3] == "e":  
            count += 1
    return count
#######################################################

# end other : 
def end_other(s1, s2):
    return s1.lower().endswith(s2.lower()) or s2.lower().endswith(s1.lower())

###########################################################
#xyz there :
def xyz_there(s):
   
    s = s.replace('.xyz', '')
   
    return 'xyz' in s

########################################################
#count events :
def count_evens(nums):
    count = 0
    for num in nums:
        if num % 2 == 0:  
            count += 1    
    return count
##########################################################
# big diff : 
def big_diff(nums):
    return max(nums) - min(nums)

########################################################
#centered average :
def centered_average(nums):
    nums.sort()
    nums = nums[1:-1] 
    return sum(nums) // len(nums)  
######################################################
#sum 13:
def sum13(nums):
    total = 0
    i = 0
    while i < len(nums):
        if nums[i] == 13:
            i += 2  
        else:
            total += nums[i] 
            i += 1 
    return total

#####################################################
#sum67 : 
def sum67(nums):
    total = 0
    skip = False 
    for num in nums:
        if skip:
            if num == 7:
                skip = False
            continue
        if num == 6:
            skip = True 
            continue
        total += num 
    return total

##################################################
#has 22: 
def has22(nums):
    return '22' in ''.join(map(str, nums))

###################################################

#LOGIC -2 

####################################################
#make bricks :
def make_bricks(small, big, goal):
    
    max_big_bricks = goal // 5  
    big_bricks_used = min(max_big_bricks, big) 
    remaining_goal = goal - big_bricks_used * 5
    
  
    return remaining_goal <= small  

#####################################################
#lone sum :
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
##################################################
#lucky sum : 
def lucky_sum(a, b, c):
    if a == 13:
        return 0
    if b == 13:
        return a
    if c == 13:
        return a + b
    return a + b + c
##########################################
#round sum :
def round_sum(a, b, c):
    return round10(a) + round10(b) + round10(c)

def round10(num):
    if num % 10 >= 5:
        return num + (10 - num % 10)
    else:
        return num - (num % 10)

##############################################
#close far: 
def close_far(a, b, c):
    return (
        (abs(a - b) <= 1 and abs(a - c) >= 2 and abs(b - c) >= 2) or
        (abs(a - c) <= 1 and abs(a - b) >= 2 and abs(b - c) >= 2)
    )
###################################################
#make chocolate :
def make_chocolate(small, big, goal):
    big_bars = min(goal // 5, big)
    remaining = goal - big_bars * 5
    return remaining if remaining <= small else -1
#####################################################

#DONE !!!!:))