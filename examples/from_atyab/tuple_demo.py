# Paranthesis -> ()

# A Collection of Constants (Immutable)
DAYS_IN_WEEK = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")
b = list(DAYS_IN_WEEK)

# Constant (Immutable) - Use UPPERCASE Letters for variable names
SCRIPT_NAME = "tuple_demo.py"

for item in DAYS_IN_WEEK:
  print(item)

print(b)
c = tuple(b)
print(c)

d = [(1,)]
e = (1,)

print(d)
print(e)

print(type(d))
print(type(e))

print(DAYS_IN_WEEK[0:3:1])

DAYS_IN_WEEK = tuple(list(DAYS_IN_WEEK) + ["SUPER_SUNDAY"])
print(DAYS_IN_WEEK)
