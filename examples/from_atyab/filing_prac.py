import os

DATA_FILE_PATH = "./data.txt"

# data_file = open(DATA_FILE_PATH, "a")

try:
  with open(DATA_FILE_PATH, "r") as data_file:
    for line in data_file.readlines():
      print(line.strip())
except Exception as ex_obj:
  print(f"Something went wrong with the file: {DATA_FILE_PATH}", ex_obj)

print("END OF SCRIPT")

