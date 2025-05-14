#Sleep in task:
def sleep_in(weekday, vacation):
  if not weekday or vacation:
    return True
  else:
    return False
sleep_in(True,True)
###############################################################
#Monkey task :
def monkey_trouble(a_smile, b_smile):
  if a_smile == True and b_smile == True:
    return True
  elif a_smile == False and b_smile == False:
    return True
  else:
    return False
monkey_trouble(True,True)
#Monkey task another idea to write
def monkey_trouble(a_smile, b_smile):
  if (a_smile == True and b_smile == False) or (a_smile == False and b_smile == True):
    return False
  else:
    return True
monkey_trouble(True,True)
##############################################################
#Sum double task:
def sum_double(x,y):
  if x == y:
    return 2*(x+y)
  else:
    return (x+y)
sum_double(1,2)
sum_double(3,2)
sum_double(2,2)
###############################################################
#diff21 task:
def diff21(n):
  if n <= 21:
    return (21-n)
  else:
    return (n-21)*2
###############################################################
#parrot_trouble task:
def parrot_trouble(talking, hour):
  if talking and (7>hour or hour>20) :
    return True
  else:
    return False
##############################################################
#Makes10 task:
def makes10(a, b):
  if (a == 10 ) or (b == 10 ) or (a + b == 10):
    return True
  else:
    return False
##############################################################
#Near hundered task:
def near_hundred(n):
  if (90<=n<=110) or (190<=n<=210):
    return True
  else:
    return False
##############################################################
#Pos_neg task:
def pos_neg(a, b, negative):
  if (negative == False) and (((a<0) and (b>0)) or ((a>0) and (b<0))):
    return True
  elif (negative == True) and ((a<0) and (b<0)):
    return True
  else:
    return False
###############################################################
#not_string task:
def not_string(str):
  if str.startswith("not"):
    return str
  else:
    return "not " + str
################################################################
#Missing_Char:
def missing_char(text, n):
  return text[:n] + text[n+1:]
#################################################################






