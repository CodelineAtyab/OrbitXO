import os

FILE_PATH = "./data.txt"

try:
  with open(FILE_PATH, "r") as data_file:
    for line in data_file.readlines():
      print(line.strip())
except FileNotFoundError:
    print(f"Error: The file '{FILE_PATH}' was not found.")
except PermissionError:
    print(f"Error: Permission denied when trying to read the file '{FILE_PATH}'.")
except Exception as ex_obj:
  print(f"Something went wrong with the file: {FILE_PATH}", ex_obj)