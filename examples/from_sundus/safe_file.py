def Read_File(filename):

    try:
        file = open(filename, "r")     
        content = file.read()  
        file.close()

        if not content.strip():
                print("Error: File is empty or corrupted.")
        else:
                print("File content:\n")
                print(content)

    except FileNotFoundError:
        print("Error: File not found.")
        try_backup()

    except PermissionError:
        print("Error: You don't have permission to open this file.")
        try_backup()

    except UnicodeDecodeError:
        print("Error: Could not read the file due to encoding issues.")
        try_backup()

    except Exception:
        print("Error: Something went wrong reading the file.")
        try_backup()    


def try_backup():
    answer = input("Try a backup file? (yes/no): ").lower()
    if answer == "yes":
        backup = input("Enter backup filename: ")
        Read_File(backup)
    else:
        print("Goodbye")


#MAIN PROGRAM
Read_File(r"C:/Users/admin/Desktop/orbit/OrbitXO/examples/from_sundus/test_file_test.txt")                

