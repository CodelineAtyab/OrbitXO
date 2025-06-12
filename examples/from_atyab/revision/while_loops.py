"""
char_to_print = "*"
line = ""

for i in range(5):  # Outer Loop (Iterated Rows)
  for _ in range(i):  # Iterates Column
    print(" ", end="")

  for _ in range(10):  # Iterates Column
    print("*", end="")
  
  print("")
"""
outer_counter = 0
while outer_counter < 5: # BOOLEAN EXPRESSION 
  retry_attempts = 0
  
  while retry_attempts < 5: # BOOLEAN EXPRESSION 
    print("*", end="")
    retry_attempts = retry_attempts + 1
  
  print("")
  outer_counter = outer_counter + 1

