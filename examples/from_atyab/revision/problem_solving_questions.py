# Fabonacci Series
# 0, 1, 1, 2, 3, 5, 8, 13

n = 9
second_last = 0
last = 1
sum = second_last

print(second_last)

for _ in range(n):
  second_last = last
  last = sum
  sum = second_last + last
  print(sum)

print("")
print("")
print("")
# Factorial 5!
# n = 5
# 5 * 4 * 3 * 2 * 1

n = 5
result = 1

for num in range(1, n+1):
  print(num)
  result = result * num

print(result)

# Find the Max number from a given list of numbers
# list_of_numbers = [545, 33, 2, 7, 10, 23, 4]
# max_number = list_of_numbers[0]

# for num in list_of_numbers[1:]:
#   if max_number < num:
#     max_number = num

# print(max_number)

# Selection sort
list_of_numbers = [33, 2, 7, 55, 10, 23, 4]
print(list_of_numbers)

for outer_index in range(len(list_of_numbers)):
  inner_index = outer_index

  max_number_index = inner_index
  while inner_index < len(list_of_numbers):
    print(f"{list_of_numbers[max_number_index]} < {num}")
    if list_of_numbers[max_number_index] < list_of_numbers[inner_index]:
      max_number_index = inner_index
    inner_index = inner_index + 1
  
  backup = list_of_numbers[outer_index]
  list_of_numbers[outer_index] = list_of_numbers[max_number_index]
  list_of_numbers[max_number_index] = backup
  print(f"backup={backup}  index1={outer_index} index2= {max_number_index}")
  print(list_of_numbers)