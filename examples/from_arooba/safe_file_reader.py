def read_file(Arooba_file):
    try:
        file = open(Arooba_file, "r")
        content = file.read()
        file.close()
        print(f"File read successfully: {content}")
        return content

    except FileNotFoundError:
        print("File not found:", Arooba_file)
        try:
            file = open(Arooba_file, "w")
            default_text = "This is a new file created because the original was missing.\n"
            file.write(default_text)
            file.close()
            print("A new file was created.")
            return default_text
        except Exception as e:
            print("Could not create a new file:", e)

    except PermissionError:
        print("You don't have permission to read or create the file.")

    except UnicodeDecodeError:
        print("Could not read the file due to encoding issues.")

    except Exception as e:
        print("Something else went wrong:", e)

    return None
read_file(r"C:\Users\admin\Documents\safe_file_reader.txt") # r, read as string 
read_file(r"C:\Users\admin\Documents\safe.txt")
