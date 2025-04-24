# Get input from the user
rows = int(input("Enter the number of rows: "))

# Loop to generate the pattern
for i in range(1, rows + 1):
    for j in range(1, i + 1):
        print(j, end='')
    print()  # Newline after each row