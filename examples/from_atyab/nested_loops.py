star = "*"

num_of_rows = 3
num_of_col = 3

# Outer Loop
for row in range(num_of_rows):
  # Inner Loop

  for col in range(row+1):
    print("* |", end="\b ")
  
  print("\n---------")

print("I am finally outside of the loop")
