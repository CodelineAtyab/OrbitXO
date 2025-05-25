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
except UnicodeError:
    print(f"Error: There was a problem decoding the file '{FILE_PATH}'.")
except Exception as ex_obj:
  print(f"Something went wrong with the file: {FILE_PATH}", ex_obj)

if not os.path.exists(FILE_PATH):
    try:
        with open(FILE_PATH, "w") as f:
            f.write("This is a test\n")
        print(f"Created new file: {FILE_PATH}")
    except Exception as ex:
        print(f"Error creating file: {ex}")