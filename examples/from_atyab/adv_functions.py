# Function in Python are First Class Citizens (Treat like any other object )
# Defining a function - Allocating memory for instructions
# def greet():
#   print("Hello, Team!")
#   print("Orbits!")

# # Recursion: Calling a function within itself
# def increment_by_one(num):
#   if num > 7:
#     return None

#   print(num + 1)
#   increment_by_one(num + 1)
#   print(num + 1)


# increment_by_one(5)
print("END OF ENDs ==========================")

# a = greet
# greet = "I am done pointing to a function obj"

# Calling the function
# a()
# print(greet)

# l = ["12", True, [], {}, (1,), greet]
# l[5]()

# def dump_team_name():
#   ret_val = "Code Orbit"
#   print("")

# # Substitute with the return value first and then print
# print(dump_team_name())

# def dump_msg_no_of_times(msg, count):
#   if count <= 0:
#     return
#   print(msg)
#   dump_msg_no_of_times(msg, count-1)

# dump_msg_no_of_times("Say it again!", 5)

# def pow(base, exp):
#   if exp == 0:
#     return 1
#   return base * pow(base, exp-1)

# print(pow(2, 0))
# print(pow(2, 1))
# print(pow(2, 2))
# print(pow(2, 3))


# Callback Functions
def process_all_names(names, perform_action_callback):
  mod_list_of_names = []
  for name in names:
    mod_list_of_names.append(f"[TEAM CO] {name}")
  
  perform_action_callback(mod_list_of_names)

  return mod_list_of_names


list_of_names = ["Hannan", "Muhannad", "Arooba", "Aya", "Ahmed"]

def print_the_list(input_list):
  for item in input_list:
    print(item)

process_all_names(names=list_of_names, perform_action_callback=print_the_list)
# no PRINT STATEMENTS HERE



