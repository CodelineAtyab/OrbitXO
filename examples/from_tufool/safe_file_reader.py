def read_file(file_path):
    def is_valid(content):
        if not content:
            print("The file is empty or has only whitespaces.")
            return False
        if not content[0].isalpha():
            #isalpha(): all characters in the content are alphabetic/letters
            print("Invalid file format: content does not start with a letter.")
            return False
        return True
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            print(f"File loaded: {file_path}")
            if not is_valid(data):
                raise ValueError("File format is corrupted or invalid.")
            return data
    except FileNotFoundError:
        print(f"Oops! The file was not found: {file_path}")
        new_content = "A new file is created because the original file is missing."
        with open(file_path, 'w') as file:
            file.write(new_content)
        print(f"New file is created: {file_path}")
        return new_content
    except PermissionError:
        print(f"Oops! You don't have permission to read this file: {file_path}")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An error occurred: {e}")
    return None
file_path = 'data.txt'
content = read_file(file_path)
if content is not None:
    print("File content (preview):")
    print(content[:200])
else:
    print("There's no data loaded.")


# Use try / except to catch errors when reading a file.

# Show clear error messages using print().

# Check if the content is usable (not empty or corrupt).

# Return a default value or fallback if something goes wrong.