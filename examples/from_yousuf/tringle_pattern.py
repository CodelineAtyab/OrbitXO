# User input
num_of_rows = int(input("Enter number of rows: "))

# Generate triangle pattern
for i in range(1, num_of_rows + 1):
    for j in range(1, i + 1):
        print(j, end="")
    print()


   