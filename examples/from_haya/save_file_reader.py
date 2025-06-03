def is_valid(content):
    if not content:
        print("File is empty.")
        return False
    if not content[0].isalpha():
        print("Invalid file format: content does not start with a letter.")
        return False
    return True

def read_file(file_name):
    try:
        with open(file_name, 'r') as f:
            data = f.read()
            print(f"File loaded: {file_name}")
            if not is_valid(data):
                raise ValueError
            return data
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        new_content = "This is a new file created because the original was missing."
        with open(file_name, 'w') as f:
            f.write(new_content)
        print(f"New file created: {file_name}")
        return new_content
    except PermissionError:
        print(f"No permission for file: {file_name}")
    except ValueError:
        print("Invalid file content.")
    except Exception:
        print("Something went wrong while reading the file.")
    return None

file1 = 'examples/from_haya/data.txt'

text = read_file(file1)
if text is not None:
    print("File preview:")
    print(text[:200])
else:
    print("No data loaded.")