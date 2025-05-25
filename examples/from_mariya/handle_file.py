def read_file(file_name, backup_file=None):
    try:
        file = open(file_name, "r")  
        content = file.read()
        file.close()
        print("File read successfully:")
        print(content)
        return content

    except FileNotFoundError:
        print("File not found:", file_name)
        if backup_file:
            try:
                file = open(backup_file, "r")
                content = file.read()
                file.close()
                print("Backup file read successfully:")
                print(content)
                return content
            except FileNotFoundError:
                print("Backup file also not found:", backup_file)

    except PermissionError:
        print("You don't have permission to read the file.")

    except Exception as e:
        print("Something went wrong:", e)

    return None
read_file(r"C:\Users\admin\OneDrive\Desktop\notes_for_mariya.txt") #r means: raw string