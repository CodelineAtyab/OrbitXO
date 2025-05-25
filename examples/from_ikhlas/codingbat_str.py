#CodingBat String1 Excercise:

#Ex1:
def hello_name(name):
  return "Hello " + name + "!"
print(hello_name("Bob"))    
##############################################################################

#Ex2:
def make_abba(a, b): 
  return a + b + b + a
print(make_abba("Hi","Bye"))  
print(make_abba("Yo","Alice"))
print(make_abba("What","Up"))
############################################################################

#Ex3
def make_tags(tag, word):
  return "<" + tag + ">" + word + "</" + tag + ">"
print(make_tags("i","Yay"))    
print(make_tags("i","Hello"))

#extra solution
def make_tags(tag, word):
  return "<" + tag + ">" + word + "</" + tag + ">"
print(make_tags("cite","Yay")) 
##############################################################################

#Ex4
def make_out_word(out, word):
  return out[0:2] + word + out[2:4] 
print(make_out_word("<<>>","Yay"))

#extra solution
def make_out_word(out, word):
  return out[0:2] + word + out[2:4] 
print(make_out_word("<<>>","WooHoo"))

#extra solution
def make_out_word(out, word):
  return out[0:2] + word + out[2:4]
print(make_out_word("[[]]","WooHoo"))
###############################################################################

#Ex5
def extra_end(str):
  return (str[-2:]) * 3  
print(extra_end("Hello"))
print(extra_end("ab"))
print(extra_end("Hi"))
################################################################################

#Ex6

def first_two(str):
  if len(str) > 2:
    return str[:2]
  else:
    return str
print(first_two("Hello"))
print(first_two("abcdefg"))
print(first_two("ab"))
#########################################################################

#Ex7

def first_half(str):
  return str[0:len(str)//2]    
print(first_half("WooHoo"))
print(first_half("HelloThere"))
print(first_half("abcdef"))
########################################################################

#Ex8

def without_end(str):
  return str[1:(len(str)-1)]
print(without_end("Hello"))
print(without_end("java"))
print(without_end("coding"))
######################################################################

#Ex9

def combo_string(a, b):
  if len(a) < len(b):
    s_str=a
    l_str=b
  else:
    s_str=b
    l_str=a
  return s_str + l_str + s_str
print(combo_string("Hello","Hi"))
print(combo_string("hi", "Hello"))
print(combo_string("aaa", "b"))
####################################################################

#Ex10

def non_start(a, b):
  return a[1:] + b[1:] 
print(non_start("Hello","There"))
print(non_start("java","code"))
non_start("shotl","java") 
##################################################################

#Ex11

def left2(str):
  return str[2:] + str[:2] 
print(left2("Hello"))

#another solution 
def left2(str):
  return str[2:] + str[:-3] 
print(left2("Hello"))

####################################################################
####################################################################
####################################################################

#String2 Codingbat Exercise

#Ex1
def double_char(str):
  new_str= ("")
  for ch in str:
    new_str = new_str + ch * 2
  return new_str
print(double_char("The"))
print(double_char("AAbb"))
print(double_char("Hi-There"))

###########################################################################
#Ex2
def count_hi(str):
    hi_num = str.count("hi")
    return hi_num
print(count_hi("abc hi ho"))
print(count_hi("ABChi hi"))
print(count_hi("hihi"))

##############################################################################
#Ex3
def cat_dog(str):
  cat_num = str.count("cat")
  dog_num = str.count("dog")
  return cat_num == dog_num
print(cat_dog("catdog"))
print(cat_dog("catcat"))
print(cat_dog("1cat1cadodog"))

############################################################################
#Ex4
def count_code(str):
  count = 0
  for i in range(len(str)-3):
    if str[i]=="c" and str[i+1]=="o" and str[i+3]=="e":
      count = count+1  
  return count  
print(count_code("aaacodebbb"))
print(count_code("codexxcode"))
print(count_code("cozexxcope"))

########################################################################
#Ex5 ------------- solved from the first time 
def end_other(a, b):
  a=a.lower()
  b=b.lower()
  return a.endswith(b) or b.endswith(a)
print(end_other("Hiabc","abc"))
print(end_other("AbC","HiaBc"))
print(end_other("abc","abXabc"))

########################################################################
#Ex6
def xyz_there(str):
  for i in range(len(str)-2):
    if str[i:i+3]=="xyz":
      if i==0 or str[i-1] != ".":
        return True
  return False      
print(xyz_there("abcxyz"))
print(xyz_there("abc.xyz"))
print(xyz_there("xyz.abc"))