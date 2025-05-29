import pandas as pd
import os

filepath = os.path.join(".", "data.csv")

def read_file(filepath):
    try:
        if not os.path.exists(filepath):
            with open(filepath, "w") as write_file:
                write_file.write("Name,Age\nJohn,30")
                print(f"Created a new file: {filepath}")
        
       
        if not os.access(filepath, os.R_OK):
            raise PermissionError("Permission denied: " + filepath)

       
        df = pd.read_csv(filepath)
        print("File read successfully:", filepath)
        return df

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read the file '{filepath}'")
    except UnicodeError:
        print(f"Error: There was a problem decoding the file '{filepath}'")
    except Exception as e:
        print(f"Error: Something went wrong with the file '{filepath}':", e)

    return None

print(read_file(filepath))
