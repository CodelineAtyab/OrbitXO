"""
For Loops
While Loops
Nested For Loops
Nested While Loops
List
Dict
List Comprehension
List Slicing
String Slicing
--------------
pow()
factorial()
palindrome()
sort()
max_num()
fabonaci_series()
"""

char_to_print = "*"
line = ""

for i in range(5):  # Outer Loop (Iterated Rows)
  for _ in range(i):  # Iterates Column
    print(" ", end="")

  for _ in range(10):  # Iterates Column
    print("*", end="")
  
  print("")

num_of_max_stars = 1
num_of_max_rows = 5

for row in range(num_of_max_rows):
  for _ in range(num_of_max_rows - (row + 1)):
    print(" ", end="")

  for col in range(num_of_max_stars):
    print("*", end="")
  
  num_of_max_stars = num_of_max_stars + 1
  print("")


import math

num_of_max_rows = 5
init_num = 1
prev_num = 0

for row in range(num_of_max_rows):
  for _ in range(num_of_max_rows - (row + 1)):
    print(" ", end="")

  print(int(math.pow(10, row) + prev_num) * int(math.pow(10, row) + prev_num))
  prev_num = math.pow(10, row) + prev_num

names = ["Mr.A", "Mr.B", "Mr.C"]

for name in names:
  print(name)