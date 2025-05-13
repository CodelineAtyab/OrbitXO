list_of_num = ["96892012345", "96871234507", "96858314567", "968463728", "9684637254"]
set_of_num = set(["96892012345", "96871234507", "96858314567", "968463728", "9684637254"])

user_input = "96858314567"

if user_input in set_of_num:
  print(f"Match {user_input}")

if user_input in list_of_num:
  print(f"Match {user_input}")