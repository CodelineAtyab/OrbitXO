# Read → Calculate → Filter → Write → Handle errors
with open("C:/Users/admin/Desktop/Code Orbit/Trainings/OrbitXO/examples/from_tufool/trying.txt", 'r') as file:
    lines = file.readlines()

#h = headers
#v = values
headers = [h.strip() for h in lines[0].strip().split(',')] # Strip spaces from headers
data = []
# Read the CSV file and store the data in a list of dictionaries
for line in lines[1:]:
    values = [v.strip() for v in line.strip().split(',')] # Strip spaces from values
    if len(values) == len(headers):
        row = {headers[i]: values[i] for i in range(len(headers))}
        data.append(row)

# check if a value is a number
def is_number(value):
    try:
        float(value)
        return True 
    except ValueError:
        return False
    
# Calculate min, max, and average for each numeric column
columns = list(zip(*data))
for header in headers:
    values = [row[header] for row in data if is_number(row[header])]
    numbers = [float(v) for v in values]
    if numbers:
        print(f"Column '{header}' - Min: {min(numbers)}, Max: {max(numbers)}, Avg: {sum(numbers)/len(numbers):.2f}")
    else:
        print(f"Column '{header}' contains non-numeric values.")

# Filter rows (value in column 1 is > 30)
filtered_rows = []
for row in data:
    try:
        if 'Age' in row and is_number(row['Age']):
            if float(row['Age']) > 30:
                filtered_rows.append(row)
            else:
                print(f"Skipping row due to 'Age' <= 30: {row}").islower()
    except KeyError:
        print(f"Skipping row (missing 'Age' column): {row}")
    
# Write filtered data to new CSV
with open('filtered_data.csv', 'w') as file:
    file.write(','.join(headers) + '\n') 
    for row in filtered_rows:
        file.write(','.join(row.values()) + '\n') 

# it saves the filtered rows into a new file called filtered_output.csv
print(f"Filtered data written to 'filtered_data.csv'. Total rows: {len(filtered_rows)}")

# check the output file and print its content
try:
        with open('filtered_data.csv', 'r') as file:
            lines = file.readlines()
except FileNotFoundError:
        print("The filtered data file does not exist. Please check the previous steps.")
except Exception as e:
        print(f"An error occurred while reading the filtered data file", e)
else:
        print("Filtered data file content:")
        for line in lines:
            print(line.strip())