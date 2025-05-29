# Warmup-1 > sleep_in
def sleep_in(weekday, vacation):
  if not weekday or vacation:
    return True 
  else:
    return False
  
# Warmup-1 > monkey_trouble
def monkey_trouble(a_smile, b_smile):
  if a_smile == b_smile:
    return True 
    
  if a_smile != b_smile:
    return False
  
# Warmup-1 > sum_double
def sum_double(a, b):
  if a == b:
    return 2 * (a+b)
    
  else: 
      return a + b
  
# Warmup-1 > diff21
def diff21(n):
  if n<= 21:
    return (21 - n)
  
  else: #if the value is more than 21
    return (n - 21) * 2

# Warmup-1 > parrot_trouble
def parrot_trouble(talking, hour):
  if talking and (hour <7 or hour >20):
    return True 
  else: 
    return False
  
# Warmup-1 > makes10
def makes10(a, b):
  if a== 10 or b==10 or a+b==10:
    return True
    
  else:
    return False
 # Warmup-1 > near_hundred
def near_hundred(n):
  if (abs(100-n) <=10) or (abs(200-n) <=10):
    return True
  
  else:
    return False

# Warmup-1 > pos_neg
def pos_neg(a, b, negative):
  if negative:
     return(a < 0 and b < 0)
  
  else:
    return ((a<0 and b>0) or (a>0 and b<0)) 
  
# Warmup-1 > not_string
def not_string(str):
    if str.startswith("not"):
        return str
    else:
        return "not " + str

# Warmup-1 > missing_char
def missing_char(str, n):
  f = str[:n]
  b = str[n+1:]
  return f + b 

# Warmup-1 > front_back
def front_back(str):
  if len(str) <= 1:
    return str
  else:
    return str[-1] + str[1:-1] + str[0]
  
# Warmup-1 > front3
def front3(str):
    front = str[:3] 
    return front * 3
