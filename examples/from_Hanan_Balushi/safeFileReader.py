
try:
    path = input("Enter file path: ")
    with open(path, "r") as file:
        contents = file.readlines()
        print(contents)
except FileNotFoundError:
    print("File not found! please enter correct path")
except PermissionError:
    print("Permission Denied!")
except Exception as e :
    print("The following issue occured: {e}")


