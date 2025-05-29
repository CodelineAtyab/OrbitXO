def read_file(file_name):
 
    def is_valid(content):
        if not content:
            print("The file is empty.")
            return False
        if not content[0].isalpha():
            print("Invalid file format: content does not start with a letter.")
            return False
        return True

    try:
       
        with open(file_name, 'r') as file:
            data = file.read()
            print(f"File loaded: {file_name}")

           
            if not is_valid(data):
                raise ValueError("File format is corrupted or invalid.")

            return data

    except FileNotFoundError:
       
        print(f"File not found: {file_name}")
        new_content = "A new file has been created because the original file was missing."
        with open(file_name, 'w') as file:
            file.write(new_content)
        print(f"New file created: {file_name}")
        return new_content

    except PermissionError:
       
        print(f"No permission to open the file: {file_name}")

    except ValueError as ve:
        
        print(ve)

    except Exception as e:
   
        print(f"An error occurred: {e}")

    
    return None


file_name = 'data.txt'


content = read_file(file_name)

if content is not None:
    print("File content (preview):")
    print(content[:200])  
else:
    print("No data was loaded.")
