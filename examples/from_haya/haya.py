# Get the number of rows from the user
num_of_rows = int(input("Enter the number of rows: "))

# Loop through each row
for i in range(1, num_of_rows + 1):
    # Initialize an empty string for the current row
    row_output = ""
    # Add numbers from 1 up to the current row number
    for j in range(1, i + 1):
        row_output += str(j)
    # Print the current row
    print(row_output)
