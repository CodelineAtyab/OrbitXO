File_Name= input("Enter the file name: ")
try:
    with open (File_Name,"r") as file:
        data=file.read()

except FileNotFoundError:
    print("File not found.")
except PermissionError:
    print("You don't have permission to read this file.")        