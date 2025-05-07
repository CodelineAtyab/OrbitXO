# List Comprehension
# 1) The loop runs (2nd iteration)
# 2) num becomes 1
# 3) Check if IF is True or False.
# 4) ONly if IF is TRUE: left hand side expression result is appended to the list automatically
list_of_num = [f"Hello {num}" for num in range(10) if num]  # Declaration and init with empty []

# even_numbers = [curr_num for curr_num in range(0, 20) if curr_num % 2 != 0]
# print(even_numbers)

# [["X", "X", "X"], ["X", "X", "X"], ["X", "X", "X"]]
board = [["X" for j in range(3)] for i in range(3)]
# print(board)

# Outer Loop
for row in board:
  # Inner Loop Runs 3 times
  for c in row:
    print(c, end="")
  print("\nInner Loop Exit")