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