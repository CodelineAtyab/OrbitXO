import sys
try:
    if sys.argv[1][-4:] == ".txt":
        path = "examples/from_sulaiman/" + sys.argv[1]
    else:
        path = "examples/from_sulaiman/" + sys.argv[1] + ".txt"
    try:
        reader = open(path, "r")
        print(reader.read())
        reader.close()
    except FileNotFoundError:
        print("file does not exsist")
    except PermissionError:
        print("You don't have a permission to open the file")
except IndexError:
    print("Missing arguments, make sure you have one for the name of the txt file")