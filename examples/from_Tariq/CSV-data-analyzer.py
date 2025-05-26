import csv
import os
import sys

def read_csv(file_path):
 try:
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    if not data:
       ("The CSV file is empty.")
       sys.exit(1)
    return data
 except FileNotFoundError:
    print(f"Error: The file {file_path} does not exist.")
 except IOError as e:
    print(f"Error reading file {file_path}: {e}")
 except PermissionError:
    print(f"Error: Permission denied when trying to read {file_path}.")
    sys.exit(1)
 except csv.Error as e:
    print(f"Error reading CSV file: {e}")
 

def calculate_min_max_avg(data, column):
   try:
        values = values = [int(row[column]) for row in data[1:] if row[column].isdigit()]
        if not values:
            return None, None, None 
        min_value = min(values)
        max_value = max(values)
        avg_value = sum(values) / len(values)
        return min_value, max_value, avg_value
   except IndexError:
        print(f"Error: Column index {column} is out of range.")
        sys.exit(1)
   except ValueError:
        print(f"Error: Non-numeric data found in column {column}.")
        sys.exit(1)
   except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
        
def filter_row_by_criteria(data, column, criteria):
    try:
        filtered_rows = [row for row in data[1:] if int(row[column]) == criteria]
        if not filtered_rows:
            print(f"No rows found matching the criteria: {criteria}")
            return []
        return filtered_rows
    except IndexError:
        print(f"Error: Column index {column} is out of range.")
        sys.exit(1)
    except ValueError:
        print(f"Error: Non-numeric data found in column {column}.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while filtering: {e}")
        sys.exit(1)

def write_results_to_csv(file_path, results):
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(results)
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when trying to write to {file_path}.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while writing to file: {e}")
        sys.exit(1)
    


PATH_FILE = 'data.csv'
if not os.path.exists(PATH_FILE):
    try:
        with open(PATH_FILE, "w") as f:
            f.write("12,23,34,45\n56,67,78,89\n90,12,34,56\n")
        print(f"Created new file: {PATH_FILE}")
    except Exception as ex:
        print(f"Error creating file: {ex}")

data = read_csv(PATH_FILE)
print("Data read from CSV file:")
for row in data:
    print(row)

column_index = sys.argv[1]
if not column_index.isdigit():
    print("Please provide a valid column index as an argument.")
    sys.exit(1)
column_index = int(column_index)
min_value, max_value, avg_value = calculate_min_max_avg(data, column_index)
print(f"Min: {min_value}, Max: {max_value}, Avg: {avg_value}")

criteria = sys.argv[2]
if criteria == "max":
    filtered_rows = filter_row_by_criteria(data, column_index, max_value)
elif criteria == "min":
    filtered_rows = filter_row_by_criteria(data, column_index, min_value)
elif criteria == "avg":
    filtered_rows = filter_row_by_criteria(data, column_index, avg_value)
else:
    print("Invalid criteria. Please use 'max', 'min', or 'avg'.")
    sys.exit(1)

output_file = 'filtered_results.csv'
write_results_to_csv(output_file, filtered_rows)
print(f"Filtered results written to {output_file}.")


