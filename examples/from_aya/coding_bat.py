def sum_double(a, b):
  if a != b: 
     sum = a + b 
     return sum 
  if a == b: 
     x = (a + b) * 2 
     return x 
 
num = sum_double(2, 2)
print(num) 


def monkey_trouble(a_smile, b_smile): 
       if a_smile and b_smile : 
           return True 
       if not a_smile and not b_smile: 
           return True 
 
monkey = monkey_trouble(True, True)
print (monkey )
            
     


def parrot_trouble(talking, hour):
  if talking == True and ( hour < 7 or hour > 20):
     return True 
  else:
     return False 
parrot_trouble = parrot_trouble(True , 6 )
print(parrot_trouble)


   

def makes10(a, b):
  return ( a == 10 or b == 10 or a+b == 10 ) 
ma0 = makes10(9, 1)
print(ma0)


def near_hundred(n):
    return (n >=90 and n <=110 ) or (n >=190 and n <210 )  

near= near_hundred(90 )
print (near)



def pos_neg(a, b, negative):
 if negative: 
    return ( a<0 and b<0 ) 
 else: 
    return ((a < 0 and b >0 ) or(a > 0 and b < 0))  
neg =pos_neg(-1 , 1 , False )
print(neg ) 


def not_string(str):  
    if str[0:4] == "not ":
        return str 
    elif str == "not": 
        return str 
    else: 
        return "not " + str 
    
 
h = not_string ( "its aya")
print(h)



def missing_char(str, n):
  return str[0:n] + str[n+1:] #first print str from 0 tell n(letter position) add n+1 position tell end

ll=missing_char("ayaa",2) 
print(ll)


def front_back(str):
  return str[-1] + str[1:-1] + str[0]

yy=front_back("bbaayan ")
print(yy)

#front3
def front3(str):
  if len(str) >= 3:
    return str[0:3]+str[0:3]+str[0:3]
  if len(str) <= 2:
    return str[0:2]+str[0:2]+str[0:2]
  else:
    return str



    
gg=front3("ASab")
print(gg) 
 

                                         
def string_times(str, n):
  return (str *n )

dd=string_times("Hello",2)
print(dd)


def front_times(str, n):
  return (str[0:3] * n) 

tt=front_times("AYA",3)
print(tt) 


def string_bits(str):
    result = ""
    for i in range(len(str)):
        if i % 2 == 0:
            result += str[i]
    return result 



ss=string_bits("Ayaan")
print(ss)


def string_splosion(str):
  result = ""
  for i in range(len(str)):
    result = result + str[:i+1]
  return result

ss=string_splosion("aya")
print(ss)




def last2(str):
  last2 =str[-2:] 
  count = 0
  for i in range(len(str)-2):
    sub = str[i:i+2]
    if sub == last2:
      count = count + 1
  return count

last=last2("ssshhhhffff")
print(last)



def array_count9(nums): 
     count = 0  
     for num in nums:
         if num == 9: 
             count += 1 
     return count 
array=array_count9([1,9,9,9]) 
print(array) 



def array_front9(nums):
    last = min(4, len(nums))
    for i in range(last):
        if nums[i] == 9:
            return True
    return False

S2=array_front9([2,3,9,3])
print(S2)


def array123(nums):
  for i in range(len(nums) - 2):
    if nums[i] == 1 and nums[i+1] == 2 and nums[i+2] == 3:
      return True
  return False

ar123=array123([1,2,3.8,1,2,3])
print(ar123)


def string_match(a, b):
  count = 0
  shorter_length = min(len(a), len(b))
    
  for i in range(shorter_length - 1):
    if a[i:i+2] == b[i:i+2]:
       count += 1
    
  return count 



def hello_name(name):
    return "Hello " + name + "!" 
name = hello_name("aya ") 
print(name)
     

def make_abba(a, b):
    return a + b + b + a 
make_abba = make_abba("aya " , "salim")
print(make_abba) 


def make_tags(tag, word):
    return "<" + tag + ">" + word + "</" + tag + ">" 
def make_tags(tag, word):
    return f"<{tag}>{word}</{tag}>"
print(make_tags("ai", "ops")) 


def make_out_word(out, word):
    return out[:2] + word + out[2:]
make_out_word= make_out_word("hello " , "aya ")
print(make_out_word)


def extra_end(str):
    return str[-2:] * 3
extra_end= extra_end("aya")
print(extra_end)


def first_two(str):
    return str[:2]
first_two = first_two ("Ayaan ") 
print(first_two)


def first_half(str):
    return str[:len(str)//2]
first_half= first_half("Ayaan")
print(first_half)
 
 
def without_end(str):
    return str[1:-1]
without_end= without_end("hello")
print(without_end) 


def combo_string(a, b):
    if len(a) < len(b):
        return a + b + a
    else:
        return b + a + b
combo_string=combo_string ("aya" , "salim")
print(combo_string)

def non_start(a, b):
    return a[1:] + b[1:]
non_start= non_start("aya " , "salim")
print(non_start)



def left2(str):
    return str[2:] + str[:2]
left2= left2("Ayann")
print(left2) 


def first_last6(nums):
    return nums[0] == 6 or nums[-1] == 6
first_last6= first_last6([1,2,3,4,5,6])
print(first_last6) 


def make_pi():
   return [3, 1, 4] 
make_pi=make_pi()
print(make_pi)


def common_end(a, b):
    return a[0] == b[0] or a[-1] == b[-1]
common_end= common_end([1,2,3] , [7,3])
print(common_end) 


def sum3(nums):
    return nums[0] + nums[1] + nums[2]
sum3=sum3([1,2,3])
print(sum3)




def rotate_left3(nums):
    return [nums[1], nums[2], nums[0]]
rotate_left3=rotate_left3([1,2,3])
print(rotate_left3)


def reverse3(nums):
    return [nums[2], nums[1], nums[0]]
reverse3=reverse3([1,2,3])
print(reverse3)

def max_end3(nums):
    max_value = max(nums[0], nums[2])
    return [max_value, max_value, max_value]
max_end3=max_end3([1,2,3])
print(max_end3)

def sum2(nums):
    return sum(nums[:2])
sum2=sum2([1,2,3])
print(sum2)


def make_ends(nums):
    return [nums[0], nums[-1]]
make_ends=make_ends([1,2,3])
print(make_ends)


def has23(nums):
    return 2 in nums or 3 in nums
has23=has23([1,2,3])
print(has23) 



def cigar_party(cigars, weekend):
    if weekend:
        return cigars >= 40
    else:
        return 40 <= cigars <= 60
cigar_party=cigar_party(50, False)
print(cigar_party)


def caught_speeding(speed, is_birthday):
    if is_birthday:
        speed -= 5

    if speed <= 60:
        return 0
    elif speed <= 80:
        return 1
    else:
        return 2 
caught_speeding=caught_speeding(65, False)
print(caught_speeding)


def sorta_sum(a, b):
    total = a + b
    if 10 <= total <= 19:
        return 20
    else:
        return total
sorta_sum=sorta_sum(10,5)
print(sorta_sum) 


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
        
alarm_clock=alarm_clock(1, False)
print(alarm_clock)


def love6(a, b):
    return a == 6 or b == 6 or (a + b) == 6 or abs(a - b) == 6
love6=love6(6, 4)
print(love6)

def in1to10(n, outside_mode):
    if outside_mode:
        return n <= 1 or n >= 10
    else:
        return 1 <= n <= 10
in1to10=in1to10 (5 , False)
print(in1to10)



def near_ten(num):
    return num % 10 <= 2 or num % 10 >= 8
near_ten=near_ten(12)
print(near_ten)


def make_bricks(small, big, goal):
    max_big = min(big, goal // 5)
    remaining = goal - (max_big * 5)
    return small >= remaining
make_bricks=make_bricks(3,1,8)
print(make_bricks)


def lone_sum(a, b, c):
    sum_val = 0
    if a != b and a != c:
        sum_val += a
    if b != a and b != c:
        sum_val += b
    if c != a and c != b:
        sum_val += c
    return sum_val
lone_sum=lone_sum(1,2,3)
print(lone_sum)



def lucky_sum(a, b, c):
    if a == 13:
        return 0
    if b == 13:
        return a
    if c == 13:
        return a + b
    return a + b + c
lucky_sum=lucky_sum(1,2,3)
print(lucky_sum)



def fix_teen(n):
    
    if 13 <= n <= 19 and n not in (15, 16):
        return 0
    return n

def no_teen_sum(a, b, c):
    
    return fix_teen(a) + fix_teen(b) + fix_teen(c) 

no_teen_sum=no_teen_sum(1,2,3)
print(no_teen_sum)
   

def round_sum(a, b, c):
    return round10(a) + round10(b) + round10(c)

def round10(num):
    if num % 10 >= 5:
        return num + (10 - num % 10)
    else:
        return num - (num % 10)
round_sum=round_sum(1,2,3)
round10=round10(1) 

print(round_sum)
print(round10)


def close_far(a, b, c):
    close_b = abs(a - b) <= 1
    close_c = abs(a - c) <= 1
    far_b = abs(a - b) >= 2 and abs(b - c) >= 2
    far_c = abs(a - c) >= 2 and abs(c - b) >= 2

    return (close_b and far_c) or (close_c and far_b)
close_far=close_far(1,2,3)
print(close_far) 


def make_chocolate(small, big, goal):
    max_big_needed = goal // 5
    big_to_use = min(big, max_big_needed)
    
    remaining = goal - (big_to_use * 5)
    
    if remaining <= small:
        return remaining
    else:
        return -1
make_chocolate=make_chocolate(3,1,8)
print(make_chocolate) 


def double_char(str):
  result = ""
  for i in range(len(str)):
    result += str[i] + str[i]
  return result 
double_char=double_char("aya")
print(double_char)

def count_hi(s):
    return s.count("hi")
count_hi=count_hi("hihihihi")
print(count_hi) 


def cat_dog(s):
    return s.count("cat") == s.count("dog")
cat_dog=cat_dog ("catdog")
print(cat_dog)


def count_code(s):
    count = 0
    for i in range(len(s) - 3):
        if s[i:i+2] == "co" and s[i+3] == "e":
            count += 1
    return count
count_code=count_code("cozcoe")
print(count_code)


def end_other(a, b):
    a = a.lower()
    b = b.lower()
    return a.endswith(b) or b.endswith(a)
end_other=end_other("abc", "ab")
print(end_other)


def xyz_there(s):
    return 'xyz' in s.replace('.xyz', '')
xyz_there=xyz_there("acc.xyz")
print(xyz_there)


def count_evens(nums):
    count = 0
    for num in nums:
        if num % 2 == 0:
            count += 1
    return count
count_evens=count_evens([1,2,3,4])
print(count_evens)


def big_diff(nums):
    return max(nums) - min(nums)
big_diff=big_diff([1,2,3,4])
print(big_diff)


def centered_average(nums):
    nums_sorted = sorted(nums)          
    trimmed = nums_sorted[1:-1]     
    return sum(trimmed) // len(trimmed)
centered_average=centered_average([1,2,3,4])
print(centered_average)



def sum13(nums):
    total = 0
    skip = False

    for num in nums:
        if skip:
            skip = False  
            continue
        if num == 13:
            skip = True   
            continue
        total += num

    return total
sum13=sum13([1,2,3,4])
print(sum13)



def sum67(nums):
    total = 0
    in_ignore = False

    for num in nums:
        if num == 6:
            in_ignore = True  
        elif in_ignore:
            if num == 7:
                in_ignore = False  
        else:
            total += num 

    return total
sum67=sum67([1,2,3,4])
print(sum67)


def has22(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 2 and nums[i + 1] == 2:
            return True
    return False
has22=has22([1,2,2])
print(has22) 