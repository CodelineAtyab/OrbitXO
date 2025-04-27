# Triangle pattern script
def main():
    # Input validation for positive integer
    while True:
        try:
            num_of_rows = int(input("Enter the number of rows: "))
            if num_of_rows <= 0:
                print("Please enter a positive integer greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    # Generating the triangle pattern
    for i in range(1, num_of_rows + 1):
        # Print numbers from 1 to i
        print("".join(str(x) for x in range(1, i + 1)))

if __name__ == "__main__":
    main()
