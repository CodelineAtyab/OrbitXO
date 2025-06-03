file_name = "data.txt"

def read_file(file_name): 
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        with open(file_name, 'w') as file:
            new_content = "A new file has been created because the original file was missing."
            file.write(new_content)
        print(f"New file created: {file_name}")
    except PermissionError:  
        print(f"No permission to open the file: {file_name}")
    except ValueError as ve:    
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    except PermissionError:
        raise ValueError(f"No permission to read the file '{file_name}'.")
    return None


content = read_file(file_name)
if content is not None:
    print("File content")
    print(content)
else:
    print("No content to display.")
    










