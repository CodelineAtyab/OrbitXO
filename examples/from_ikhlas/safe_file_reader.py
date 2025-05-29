import os 

def read_data_file(file_name):
    def is_valid(content):   #content is not  empty
        if not content:
            print("The file is empty")
            return False
        if not content[0].isalpha():  #content start with a letter
            print("File does not start with a letter")
            return False
        return True

    try:   # check the file exists before open it
        if not os.path.exists(file_name):   # to returns true if the file does not exist
            raise FileNotFoundError

        with open(file_name,'r') as f:
            data = f.read()
            print(f"File loaded: {file_name}")

            if not is_valid(data):
                raise ValueError("Invalid content")

            return data

    except FileNotFoundError:
        print(f"File not found: {file_name}")
        new_content = "Here is new file created because the original was not found"
        with open(file_name,'w') as f:   #overwrite not existing file
            f.write(new_content)
        print(f"New file created: {file_name}")
        return new_content

    except PermissionError:  # file dosen't have rquired permission
        print(f"Permission denied: {file_name}")

    except ValueError as ve:
        print(f"Validation error is: {ve}")

    except Exception as e:
        print(f"Unexpected error is: {e}")

    return None

# example : I created my own text file with content "This is my example data file for testing!"
my_file="C:/Users/admin/Desktop/example_data.txt"
text=read_data_file(my_file)

if text is not None:
    print("\nFile Preview:")
    print(text[:100])  # Show first 100 characters
else:
    print("There is no data loaded")
