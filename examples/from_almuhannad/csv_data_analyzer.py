import os
import csv
import sys


if len(sys.argv) < 3:
    print("Usage: python script.py <column_index> <criteria: min | max | avg>")
    sys.exit(1)

def read_csv_file(filepath):
    try:
        with open(filepath, 'r') as file:
            file_reader = csv.reader(file)
            data = [row for row in file_reader]
            if not data:
                print("The CSV file is empty.")
                sys.exit(1)
            return data
    except FileNotFoundError:
        print(f"Error: The file {filepath} does not exist.")
    except IOError as o:
        print(f"Error reading file {filepath}: {o}")
    except PermissionError:
        print(f"Error: Permission denied when trying to read {filepath}.")
    except csv.Error as csv_error:
        print(f"Error reading CSV file: {csv_error}")

def calc_min_max_avg(data, column):
    try:
        values = [int(row[column]) for row in data[1:] if row[column].isdigit()]
        if not values:
            return None,None,None
        else:
            min_numbers = min(values)
            max_numbers  = max(values)
            avg_numbers = sum(values)/len(values)
            return min_numbers,max_numbers,avg_numbers
    except IndexError:
        print(f"Error: Column index {column} is out of range.")
    except ValueError:
        print(f"Error: Non-numeric data found in column {column}.")
    except Exception as Ex:
        print(f"An unexpected error occurred: {Ex}")

def filter_row_by_crateria(data, column, crateria):
    try:
        crateria = int(crateria)
        filtered_values = [row for row in data[1:] if int(row[column]) == crateria]

        if not filtered_values:
            print(f"No rows found matching the crateria: {crateria}")
            return []

        return filtered_values

    except IndexError:
        print(f"Error: Column index {column} is out of range.")
        return []
    except ValueError:
        print(f"Error: Non-numeric data found in column {column} or crateria.")
        return []
    except Exception as ex:
        print(f"An unexpected error occurred while filtering: {ex}")
        return []



def write_results(filepath, results):
    try:
        with open(filepath, "w") as file:
            write = csv.writer(file)
            write.writerows(results)
    except IOError as Io:
        print(f"Error writing to file {filepath}: {Io}")
    except PermissionError:
        print(f"Error: Permission denied when trying to write to {filepath}.")
    except Exception as eEx:
        print(f"An unexpected error occurred while writing to file: {eEx}")

pathfile = r".\examples\from_almuhannad\data.csv"
if not os.path.exists(pathfile):
    try:
        with open(pathfile, "w") as f:
            f.write("15,19,20,44\n88,84,38,75\n96,82,81,85\n")
            print(f"Created new file: {pathfile}")
    except Exception as ex:
        print(f"Error creating file: {ex}")

data = read_csv_file(pathfile)
print("Data read from csv file:")
for row in data:
    print(row)

column_index = sys.argv[1]
if not column_index.isdigit():
    print("Provide a valid column index!!")
column_index = int(column_index)
min_value, max_value, avg_value = calc_min_max_avg(data, column_index)
print(f"Min: {min_value}, Max: {max_value}, Avg: {avg_value}")

criteria = sys.argv[2]
if criteria == "max":
    filter_rows = filter_row_by_crateria(data,column_index,max_value)
elif criteria == "min":
    filter_rows = filter_row_by_crateria(data, column_index, min_value)
elif criteria == "avg":
    filter_rows = filter_row_by_crateria(data, column_index, avg_value)
else:
    print("Invalid criteria. Please use 'max', 'min', or 'avg'.")
    sys.exit(1)

save_file = r".\examples\from_almuhannad\filtered_results.csv"
write_results(save_file, filter_rows)
print(f"Filtered results written to {save_file}.")