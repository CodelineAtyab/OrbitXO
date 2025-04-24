def print_triangle_pattern(num_of_rows):
    number = 1
    for row in range(1, num_of_rows + 1):
        for col in range(1, row + 1):
            print(number, end=" ")
            number += 1
        print()  # Move to the next line after each row

if __name__ == "__main__":
    try:
        num_of_rows = int(input("Enter the number of rows: "))
        if num_of_rows < 1:
            print("Please enter a positive integer greater than 0.")
        else:
            print("\nGenerated Triangle Pattern:\n")
            print_triangle_pattern(num_of_rows)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")