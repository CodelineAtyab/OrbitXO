#CodingBat Logic1 Excercise:

#Ex1
def cigar_party(cigars, is_weekend):
  if is_weekend:  
    if cigars>=40:
      return True
    else:
      return False
  else:
    if cigars>=40 and cigars <=60:
      return True
    else:
      return False
print(cigar_party(30,False))
print(cigar_party(50,False))
print(cigar_party(70,True))

###############################################################################

#Ex2
def date_fashion(you, date):
    if you <=2 or date <=2:
      return 0
    elif you >=8 or date >=8:
      return 2
    else:
      return 1

print(date_fashion(5,10))
print(date_fashion(5,2))
print(date_fashion(5,5))

##################################################################################

#Ex3
def squirrel_play(temp, is_summer):
  if is_summer:
    if temp>=60 and temp<=100:
      return True
    else:
      return False
      
  else:
    
    if temp>=60 and temp<=90:
      return True
    else:
      return False
print(squirrel_play(70,False))
print(squirrel_play(95,False))
print(squirrel_play(95,True))

################################################################################

#Ex4
def caught_speeding(speed, is_birthday):
  if is_birthday:
    speed = speed - 5
  if speed<=60:
    return 0
  elif speed>=61 and speed<=80:
    return 1
  else:
    return 2
print(caught_speeding(60,False))
print(caught_speeding(65,False))
print(caught_speeding(65,True))

###############################################################################

#Ex5
def sorta_sum(a, b):
  result = a+b
  if result>=10 and result<=19:
    return 20
  else:
    return result 
print(sorta_sum(3,4))
print(sorta_sum(9,4))
print(sorta_sum(10,11))

###############################################################################

#Ex6
def alarm_clock(day, vacation):
  if vacation:
    if day==0 or day==6:
      return "off"
    else:
      return "10:00"
  else:
    if day==0 or day==6:
      return "10:00"
    else:
      return "7:00"
print(alarm_clock(1,False))
print(alarm_clock(5,False))
print(alarm_clock(0,False))

###################################################################

#Ex7
def love6(a, b):
  sum=a+b
  sub=abs(a-b)
  if a==6 or b==6:
    return True
  elif sum==6:
    return True
  elif sub==6:
    return True
  else:
    return False
print(love6(6,4))
print(love6(4,5))
print(love6(1,5))    

####################################################################

#Ex8
def in1to10(n, outside_mode):
  if outside_mode:
    if n<=1 or n>=10:
      return True
    else:
      return False
  else:  
    if n>=1 and n<=10:
      return True
    else:
      return False
print(in1to10(5,False))
print(in1to10(11,False))
print(in1to10(11,True))

############################################################################

#Ex9
def near_ten(num):
  reminder = num % 10
  if reminder<=2 or reminder>=8:
    return True
  else:
    return False
print(near_ten(12))
print(near_ten(17)) 
print(near_ten(19))

#Another solution using list:
def near_ten(num):
  reminder = num % 10
  if reminder in [0,1,2,9,8]:
    return True
  else:
    return False
print(near_ten(12))
print(near_ten(17)) 
print(near_ten(19))

#################################################################
#################################################################
#################################################################
#CodingBat Logic2 Excercise:

#Ex1
def make_bricks(small, big, goal):
  big_bricks= goal // 5
  big_bricks_used= min (big,big_bricks)
  length = (big_bricks_used * 5)
  rem_length = goal - length
  if small>= rem_length:
    return True
  else:
    return False
print(make_bricks(3,1,8))
print(make_bricks(3,1,9))
print(make_bricks(3,2,10))

#################################################################

#Ex2
def lone_sum(a, b, c):
  sum=0
  if a!=b and a!=c:
     sum=sum + a
  if b!=a and b!=c:
     sum=sum + b
  if c!=a and c!=b:
     sum=sum + c
  return sum
print(lone_sum(1,2,3))
print(lone_sum(3,2,3))
print(lone_sum(3,3,3))

##################################################################

#Ex3
def lucky_sum(a, b, c):
  if a == 13:
    return 0
  if b == 13:
    return a
  if c == 13:
    return a+b
  return a+b+c 
print(lucky_sum(1,2,3))
print(lucky_sum(1,2,13))
print(lucky_sum(1,13,3))

###########################################################

#Ex4
def no_teen_sum(a, b, c):
  sum=0
  if a in range(13,20) and a !=15 and a !=16:
        a=0
  if b in range(13,20) and b !=15 and b !=16:
        b=0
  if c in range(13,20) and c !=15 and c !=16:
        c=0
  return a+b+c
def fix_teen(n):
  if n in range(13,20) and n !=15 and n !=16:
    return 0
  else:
    return n    
print(no_teen_sum(1,2,3))
print(no_teen_sum(2,13,1))   
print(no_teen_sum(2,1,14))

################################################################

#Ex5
def round_sum(a, b, c):
  round_a=round10(a)
  round_b=round10(b)
  round_c=round10(c)
  return round_a+round_b+round_c
  
def round10(num):
  if num%10>=5:
    return num + (10-num%10)
  else:
    return num - num%10
print(round_sum(16,17,18))
print(round_sum(12,13,14))
print(round_sum(6,4,4))

##############################################################

#Ex6
def close_far(a, b, c):
  a_close_b = abs(a-b) <=1
  a_close_c = abs(a-c) <=1
  a_far_b = abs(a-b) >=2
  a_far_c = abs(a-c) >=2
  b_far_c = abs(b-c) >=2
  
  return (a_close_b and a_far_c and b_far_c) or (a_close_c and a_far_b and b_far_c)
print(close_far(1,2,10))
print(close_far(1,2,3))
print(close_far(4,1,3))

##################################################################

#Ex7
def make_chocolate(small, big, goal):
  big_bars = min(goal//5, big)
  remaining= goal - (big_bars*5)
  if small >= remaining:
    return remaining
  else:
    return -1
print(make_chocolate(4,1,9))
print(make_chocolate(4,1,10))
print(make_chocolate(4,1,7)) 