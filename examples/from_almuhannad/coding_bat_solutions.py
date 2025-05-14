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

  