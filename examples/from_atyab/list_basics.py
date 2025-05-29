# WHY LISTS ?????

# Naming each variable
team_member_name_1 = "Hanan"
team_member_name_2 = "Muzna"
team_member_name_3 = "Fatma"
team_member_name_4 = "Muhannad"
team_member_name_5 = "Tariq"


# Naming the collection
list_of_names = []
list_of_names.append("Hanan")
list_of_names.append("Muzna")
list_of_names.append("Fatma")
list_of_names.append("Muhannad")
list_of_names.append("Fatma")
list_of_names.append("Tariq")

# for num in range(0, 5):
#   list_of_names.append(num)

# list_of_names.append(["A", "B", [1, 2, 3], "D"])

# for name in list_of_names:
#   print(f"Name: {name}")

# ran_list = list_of_names[-1]
# middle_elem_index = len(ran_list) // 2
# num_list = ran_list[middle_elem_index]

# print(num_list[1])

# for name_count in range(0, list_of_names.count("Fatma")):
#   index = list_of_names.index("Fatma")
#   del list_of_names[index]

# mod_list = []
# for name in list_of_names:
#   if name != "Fatma":
#     print(name)
#     mod_list.append(name)

# list_of_names = mod_list
# print(list_of_names)

# print([name for name in list_of_names if name != "Fatma"])

x = list_of_names[0]
del list_of_names[0]

x = list_of_names.pop(1)
print(x)

# I have list of numbers and I want to filter Even numbers
list_of_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filtered_even_numbers = []
filtered_odd_numbers = []

for num in list_of_numbers:
  if num % 2 == 0:
    filtered_even_numbers.append(num)
  else:
    filtered_odd_numbers.append(num)

print(filtered_even_numbers)
print(filtered_odd_numbers)

# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# steps = 1
# [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# steps = 2
# [9, 10, 1, 2, 3, 4, 5, 6, 7, 8]