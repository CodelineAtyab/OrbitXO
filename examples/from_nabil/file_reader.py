import os

File_Path = "./data.txt"

try:
  with open(File_Path, "r") as file_data:
    for i in file_data.readlines():
      print(i.strip())

except FileNotFoundError:
    print(f"Error: The file not found'{File_Path}'.")

except PermissionError:
    print(f"Error: you dont have permission to read the file '{File_Path}'.")

except UnicodeError:
    print(f"Error: Terror in decoding the file '{File_Path}'.")

except Exception as ex_obj:
  print(f"Something went wrong with the file: {File_Path}", ex_obj)


if not os.path.exists(File_Path):
    try:
        with open(File_Path, "w") as f: 
                   
         f.write("This is a test\n")

        print(f"Created new file: {File_Path}")


    except Exception as ex:
        print(f"Error creating file: {ex}")
