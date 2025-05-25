import os

file_path = "./do.txt"
try:
    with open(file_path, "r") as do_file:
        for text in do_file.readlines():
            print(text.strip())
except FileNotFoundError:
    print(f"Error : the file '{file_path}' was not found.")
except PermissionError:
    print(f"Error: Permission denied when trying to read the file '{File_Path}'")
except UnicodeError:
    print(f"Error: There was a problem decoding the file '{file_path}' ")
except Exception as ex_do:
    print(f"Error : Something went wrong with the file: {file_path}", ex_do)


if not os.path.exists(file_path):
    try:
        with open(file_path, "w") as write_file:
            write_file.write("This is to do list")
            print (f"Created a new file: {file_path}")
    except Exception as ex:
        print(f"Error Creating file: {ex}")

          