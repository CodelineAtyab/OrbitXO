# sleepin task 

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
  