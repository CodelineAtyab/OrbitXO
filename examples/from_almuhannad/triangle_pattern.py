def print_triangle(num_of_rows):
    current_num = 1
    for row in range(1, num_of_rows + 1):
        for _ in range(row):
            print(current_num, end=' ')
            current_num += 1
        print()  # Move to the next line
def main():
    try:
        num_of_rows = int(input("Enter the number of rows: "))
        if num_of_rows <= 0:
            print("Please enter a positive integer.")
        else:
            print_triangle(num_of_rows)
    except ValueError:
        print("Invalid input. Please enter an integer.")
if __name__ == "__main__":
    main()