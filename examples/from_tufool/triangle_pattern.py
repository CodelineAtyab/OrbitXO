user_input = input("Enter number of rows: ")

num_of_rows = int(user_input)

for i in range(num_of_rows):
    for num in range(i + 1):
        print(num + 1, end="")
    print()