import os 

# example:I created my own text file with content "This is my example data file for testing!"

my_file="C:/Users/admin/Desktop/example_data.txt"

def is_valid(content):  #content is not empty
    if not content:
        print("The file is empty")
        return False
    return True

try:   # check the file exists before open it
    with open(my_file,'r') as f:
            data = f.read()
            print(f"File loaded: {my_file}")

            if not is_valid(data):
                raise ValueError("Invalid content")

except PermissionError:  # file dosen't have rquired permission
    print(f"Permission denied: {my_file}")

except ValueError as ve:
    print(f"Validation error is: {ve}")

except Exception as e:
        print(f"Unexpected error is: {e}")

if data is not None:
    print("\nFile Preview:")
    print(data) 
else:
    print("There is no data loaded")
