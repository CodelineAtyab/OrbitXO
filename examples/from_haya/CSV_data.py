import csv

# Function to check if a value is a number
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Step 1: Save sample data
data = [
    "Name,Age,Salary",
    "haya,26,50000",
    "marya,24,60000",
    "muzna,24,65000",
    "aya,22,45000",
    "arooba,24,52000"
]

# Write data to a CSV file
with open("data.csv", "w", newline="") as file:
    for line in data:
        file.write(line + "\n")

# Step 2: Read CSV file and detect if it has a header
with open("data.csv", "r") as file:
    first_line = file.readline().strip()
    has_header = any(char.isalpha() for char in first_line)
    file.seek(0)  # Go back to start of file
    
    reader = csv.reader(file)

    if has_header:
        headers = next(reader)
    else:
        headers = ["Column1", "Column2", "Column3"]

    # Set up lists to hold numeric data
    numeric_data = {header: [] for header in headers}
    filtered_rows = []

    for row in reader:
        for i in range(len(row)):
            value = row[i]
            header = headers[i]

            # If it's a number, add it to the numeric_data dictionary
            if is_number(value):
                numeric_data[header].append(float(value))

        # Filter: Keep rows where Age > 22 (if 'Age' column exists)
        try:
            age_index = headers.index("Age")
            if float(row[age_index]) > 22:
                filtered_rows.append(row)
        except (ValueError, IndexError):
            pass  # Ignore errors if 'Age' column missing or invalid data

# Step 3: Show results for numeric columns
for header, values in numeric_data.items():
    if values:  # Only show if there are numbers collected for this column
        print(f"{header}: Min = {min(values)}, Max = {max(values)}, Avg = {sum(values)/len(values):.2f}")

# Step 4: Write filtered rows to a new CSV file
with open("filtered_output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    if has_header:
        writer.writerow(headers)
    writer.writerows(filtered_rows)

print("Filtered data saved to filtered_output.csv")
