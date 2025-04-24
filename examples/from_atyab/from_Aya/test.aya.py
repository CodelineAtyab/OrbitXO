
# Get input from the user
num_of_rows = int(input("Enter the number of rows: "))

# Loop through each row
for i in range(1, num_of_rows + 1):
    # Print numbers from 1 to i in the same line
    for j in range(1, i + 1):
        print(j, end='')
    print()  # Move to the next line
