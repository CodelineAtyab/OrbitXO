              ################### Warmup-1 #####################

#Sleep in ************************
def sleep_in (weekday, vacation):
  if not weekday or vacation:  #not will distributed 
    return True
  else:
    return False
x= sleep_in (False, False)
print(x)

#Deff21 ********************
def diff21():
  n= int(input("Enter number:"))
  if n<= 21:
    print(abs(n-21)) 
  else:
    print(abs(21-n)*2)
diff21()

# monkey_trouble ****************************** 
def monkey_trouble(a_smile, b_smile):
  if a_smile == b_smile:
    return True
  else:
    a_smile != b_smile
    return False
print(monkey_trouble(True,False))

#sum_double ******************
def sum_double(a, b):
     if a==b:
        print((a+b)*2)
     else:
        print(a+b)
sum_double(2,2)         # this 2 number assign to above virables a,b 

# parrot_trouble**********************
def parrot_trouble(talking, hour):
    if talking and(7>hour or hour>20):
      return True
    else:
      return False   
print(parrot_trouble(True,6)) #7 and 20 not incloude 

# makes10*****************
def makes10(a, b):
  if (a ==10 or b ==10) or (a+b== 10):
    return True 
  else:
    return False
print(makes10(1,1))

#near_hundred ***********************  
def near_hundred(n):
  if (abs(n-100)<=10) or (abs(n-200)<=10):  #abs||: It is covert the nagative num to positive num.
    return True 
  else:
    return False 
print(near_hundred(93))  # True  (within 7 of 100)
print(near_hundred(90))  # True  (within 10 of 100)
print(near_hundred(89))  # False (11 more than 10 away from 100 and 200)

#pos_neg ********************************
def pos_neg(a, b, negative):
  if negative:
    return a<0 and b<0
  else:
    return (a>0 and b<0) or  (a<0 and b>0)
print(pos_neg(1,-1,False))

# not_string *************************
def not_string(str):
  if str.startswith("not"):
    return str
  else:
   return "not" +" " + str
print(not_string("candy"))
print(not_string("not"))
    
# missing_char ********************
def missing_char(str, n):
    print("codeline lenth: ", len("codeline"))
    return str[0:n]+ str[n+1:]
print(missing_char("codeline",3))

#  front_back **********************
def front_back(str):
  if len(str)<=1:
    return str
  else:
    return str[-1]+ str[1:-1]+ str[0]
print(front_back("Codeline"))

# front3 **************************
def front3(str):
  if len(str)<=3:
    return str*3
  else:
    return str[0:3]*3
print(front3("Arooba"))
print(front3("abc")) 


           ################### Warmup-2 ######################

# string_times *******************
def string_times(str, n):
  return str*n
print(string_times("Arooba",2))

# front_times *******************
def front_times(str, n):
  if len(str)<=3:
   return str*n
  else:
    return str[:3]*n
print(front_times("cod",3))
print(front_times("Python",4))

# string_bits *****************
def string_bits(str):
  return str[::2]       # [::n] n= number of steps
print(string_bits("Arooba"))

# string_splosion ******************
def string_splosion(str):
    result= ""
    for i in range(len(str)):
        result += str[:i+1]
    return result
print(string_splosion("code"))

# last2 ***********************
def last2(s):
    if len(s) < 2:
        return 0
    last2_sub = s[-2:]
    count = 0
    for i in range(len(s) - 2):
        if s[i:i+2] == last2_sub:
            count += 1
    return count

# array_count9 *****************
def array_count9(nums):
  return nums.count(9)
x= [1,2,9,9,5,9]
print(array_count9(x))

# array_front9 ***********************
def array_front9(nums):
  if 9 in nums[:4]:
    return True
  else:
    return False
print(array_front9([1,9,8,5,6]))

# array123 ****************
def array123(nums):
    for i in range(len(nums) - 2):
        if nums[i] == 1 and nums[i+1] == 2 and nums[i+2] == 3:
            return True
    return False
print(array123([1,2,3,3,5]))

# string_match ***************
def string_match(a, b):
    count = 0
    length = min(len(a), len(b))
    for i in range(length - 1):
        if a[i:i+2] == b[i:i+2]:
            count += 1
    return count

                #  ******************* String ***********************

# hello_name ************************
def hello_name(name):
    return "Hello"+ "" +name+"!"
print(hello_name(" Arooba"))

# make_abba ********************
def make_abba(a, b):
  return (str(a)+ str(b))+ (str(b)+ str(a))
print(make_abba("Hi","Arooba"))

# make_tags *******************
def make_tags(tag, word):
  return "<"+ tag+ ">"+ word+ "</"+ tag+ ">" 
print(make_tags("i", "Arooba"))

# make_out_word *****************
def make_out_word(out, word):
  return out[:2]+ word + out [2:]
print(make_out_word("(())","codeline"))

# extra_end ****************
def extra_end(str):
  return str[-2:]*3
print(extra_end("code"))

# first_two *********************
def first_two(str):
  return str[0:2]
print(first_two("codeline"))

#  first_half *************
def first_half(str):
  x= len(str)//2    #Integer division: 7 // 2= 3 &  egular division:	7 / 2= 3.5
  return str[0:x] 
print(first_half("codeline"))

# without_end **************
def without_end(str):
  return str[1:-1]
print(without_end("codeline"))

# combo_string **************
def combo_string(a, b):
  if len(a)>len(b):
    return b+a+b
  else:
    return a+b+a
print(combo_string("Arooba","codeline"))

# non_start **************
def non_start(a, b):
  return a[1:]+b[1:]
print(non_start("Hello", "There"))

# left2 **************
def left2(str):
  if len(str)<=2:
    return str
  else:
    x=len(str)//2
    return str[2:] + str[:2]
print(left2("Hello"))  # "lloHe"


            #    ******************** list-1 ****************************


# first_last6 ******************
def first_last6(nums):
  return nums[0]==6 or nums[-1]==6
print(first_last6([1,2,6,3,6]))  # True

# same_first_last *******************
def same_first_last(nums):
  return ((len(nums)>=1) and (nums[0]==nums[-1]))
print(same_first_last([1,2,3,4,5]))  # False

# make_pi ********************
def make_pi():
  return [3,1,4]
print(make_pi())  # [3, 1, 4]

# common_end ************************
def common_end(a, b):
  return (len(a)>=1 and len(b)>=1) and ((a[0]==b[0]) or (a[-1]==b[-1]))

# sum3 ****************
def sum3(nums):
  return nums[0]+ nums[1]+nums[2]
print(sum3([1,2,3]))  # 6

# rotate_left3 **************
def rotate_left3(nums):
  return [nums[1],nums[2],nums[0]]

# reverse3 ***************
def reverse3(nums):
  return [nums[2],nums[1],nums[0]]
print(reverse3([1,2,3]))  # [3, 2, 1]

# max_end3 *****************
def max_end3(nums):
  if (len(nums)==3) and (nums[0]>nums[-1]):
    return [nums[0],nums[0],nums[0]]
  else:
    return [nums[-1],nums[-1],nums[-1]]

# sum2*****************
def sum2(nums):
  if len(nums)>=2:
    return nums[0]+nums[1]
  elif len(nums)==1:
      return nums[0]
  else:
    return 0
print(sum2([1,2,3,4,5]))  # 3

# middle_way ****************
def middle_way(a, b):
  return [a[1],b[1]]
print(middle_way([1,2,3],[4,5,6]))  

# make_ends ***************
def make_ends(nums):
  return [nums[0],nums[-1]]
print(make_ends([1,2,3]))  # [1, 3]

# has23 ******************
def has23(nums):
  if 2 in nums or 3 in nums:
    return True 
  else:
    return False
print(has23([2, 5]))  # True


        #  ********************** Logic-1 *********************

# cigar_party ******************
def cigar_party(cigars, is_weekend):
  if is_weekend:
    return cigars>=40
  else:
    return 40<=cigars<=60

# date_fashion **************
def date_fashion(you, date):
  if ((you<=2) or (date<=2)):
    return 0
  elif ((you>=8) or (date>=8)):
    return 2
  else:
    return 1
print(date_fashion(5, 5))  # 1  

# squirrel_play ***************
def squirrel_play(temp, is_summer):
  if is_summer== False:
    return 60<=temp<=90
  elif is_summer:
    return 60<=temp<=100
  else:
    return False

# caught_speeding ********************
def caught_speeding(speed, is_birthday):
  if is_birthday:
    speed -=5
  if speed<=60:
    return 0
  elif 61<= speed <=80:
    return 1
  else:
    speed>=81
    return 2
print(caught_speeding(60, False))  # 0
print(caught_speeding(90, False))  # 2
print(caught_speeding(65, True))

# sorta_sum ******************
def sorta_sum(a, b):
  if a+b in range(10,20):
    return 20
  else:
    return a+b

# alarm_clock **********************
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

# love6 *********************
def love6(a, b):
  if a==6 or b==6 or a+b==6 or abs(a-b)==6:
    return True
  else:
    return False
print(love6(6, 4))  # True

# in1to10 **********************
def in1to10(n, outside_mode):
  if outside_mode:
    return n<=1 or n>=10
  else:
    return 1<=n<=10
print(in1to10(5, False))  # True

# near_ten **********************
def near_ten(num):
  return num % 10 in [0, 1, 2, 8, 9]
print(near_ten(12))  # True


        #   ********************* Logic-2 ************************

# make_bricks ******************
def make_bricks(small, big, goal):
    max_big = min(goal // 5, big)
    remaining = goal - (max_big * 5)
    return remaining <= small
print(make_bricks(3, 1, 8))  # True

# lone_sum **********************
def lone_sum(a, b, c):
  if a==b==c:
    return 0
  elif a==b:
    return c
  elif a==c:
    return b
  elif b==c:
    return a
  else:
    return a+b+c
print(lone_sum(1, 2, 3))  # 6
print(lone_sum(3, 2, 3))  # 2
print(lone_sum(3, 3, 3))  # 0

# lucky_sum **********************
def lucky_sum(a, b, c):
  if a==13:
    return 0
  elif b==13:
    return a
  elif c==13:
    return a+b
  else:
    return a+b+c
print(lucky_sum(1, 2, 3))  # 6
print(lucky_sum(1, 2, 13))  # 3
print(lucky_sum(1, 13, 3))  # 1

# no_teen_sum **********************
def no_teen_sum(a, b, c):
    for_teen = lambda n: 0 if n in [13, 14, 17, 18, 19] else n
    return for_teen(a) + for_teen(b) + for_teen(c)
print(no_teen_sum(1, 2, 3))  # 6

# round_sum **********************
def round_sum(a, b, c):
    return round10(a) + round10(b) + round10(c)
def round10(num):
    if num % 10 >= 5:
        return num + (10 - num % 10)  # Round up
    else:
        return num - (num % 10)       # Round down
print(round_sum(16, 17, 18))  

#  close_far **********************
def close_far(a, b, c):
    close_b = abs(a - b) <= 1
    close_c = abs(a - c) <= 1
    far_b = abs(a - b) >= 2 and abs(b - c) >= 2
    far_c = abs(a - c) >= 2 and abs(b - c) >= 2

    return (close_b and far_c) or (close_c and far_b)
print(close_far(1, 2, 10))  # True

# make_chocolate **********************
def make_chocolate(small, big, goal):
    use_big = min(goal // 5, big)
    remaining = goal - (use_big * 5)
    if remaining <= small:
        return remaining
    else:
        return -1
print(make_chocolate(4, 1, 9))  # 4


                #    ******************* String-2 **************************

# double_char **********************
def double_char(s):
    result = ''
    for char in s:
        result += char * 2
    return result
print(double_char("Arooba"))

# count_hi **********************
def count_hi(str):
    return str.count('hi')
print(count_hi("Aroobahi hi"))

# cat_dog **********************
def cat_dog(str):
  if str.count("cat")== str.count("dog"):
    return True
  else:
    return False
print(cat_dog("helloworldcatdog"))

# count_code *************
def count_code(str):
  count =0
  for i in range(len(str)-3):   # check a 4-character starting at index i
    if str[i:i+2]=='co' and str[i+3]=='e':
      count +=1
  return count
print(count_code('aaacodebbb'))
print(count_code('codexxcode'))


# end_other ****************
def end_other(a, b):
    a = a.lower()
    b = b.lower()
    return a.endswith(b) or b.endswith(a)
print(end_other('Hiabc', 'abc'))  # True
print(end_other('AbC', 'HiaBc'))  # True

# xyz_there ***************
def xyz_there(str):
  return "xyz" in str.replace(".xyz","")
print(xyz_there("abcxyz"))  # True
print(xyz_there("abc.xyz"))  # False


            #   ******************* List-2 **********************

# count_evens **************
def count_evens(nums):          
    count = 0        
    for num in nums:
        if num % 2 == 0:       
            count += 1         
    return count               
print(count_evens([2, 1, 2, 3, 4]))

# big_diff **************
def big_diff(nums):
  return max(nums)- min(nums)
print(big_diff([10, 3, 5, 6]))

# centered_average **************
def centered_average(nums):
    nums = nums[:]  # Make a copy to avoid modifying the original list
    nums.remove(min(nums))
    nums.remove(max(nums))
    return sum(nums) // len(nums)
print(centered_average([1, 2, 3, 4, 100]))

# sum13 **************
def sum13(nums):
    total = 0
    i = 0
    while i < len(nums):
        if nums[i] == 13:
            i += 2  # Skip 13 and the number immediately after
        else:
            total += nums[i]
            i += 1
    return total
print(sum13([1, 2, 2, 1]))

# sum67 **************
def sum67(nums):
    total = 0
    skip = False
    for num in nums:
        if num == 6:
            skip = True
        elif skip:
            if num == 7:
                skip = False
        else:
            total += num
    return total
print(sum67([1, 2, 2, 6, 99, 99,7]))

# has22 **************
def has22(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 2 and nums[i + 1] == 2:
            return True
    return False
print(has22([1, 2, 2, 3]))

