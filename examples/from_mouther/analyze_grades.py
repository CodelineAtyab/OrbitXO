grades = []

while True:
    print("\nStudent Grade Tracker")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. Show statistics")
    print("4. Sort grades")
    print("5. Display all grades")
    print("6. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        grade = float(input("Enter a grade (0-100): "))
        if 0 <= grade <= 100:
            grades.append(grade)
            print("Grade added successfully!")
        else:
            print("Invalid grade. Please enter a value between 0 and 100.")

    elif choice == '2':
        if not grades:
            print("No grades to remove.")
        else:
            method = input("Remove by value or index? (v/i): ").strip().lower()
            try:
                if method == 'v':
                    value = float(input("Enter grade value to remove: "))
                    grades.remove(value)
                    print("Grade removed successfully!")
                elif method == 'i':
                    index = int(input("Enter index of grade to remove: "))
                    if 0 <= index < len(grades):
                        removed = grades.pop(index)
                        print(f"Removed grade: {removed}")
                    else:
                        print("Invalid index.")
                else:
                    print("Invalid option.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
            except Exception as e:
                print("Error:", e)

    elif choice == '3':
        if not grades:
            print("No grades available to calculate statistics.")
        else:
            average = sum(grades) / len(grades)
            print("\nStatistics:")
            print(f"Average: {average:.2f}")
            print(f"Minimum: {min(grades)}")
            print(f"Maximum: {max(grades)}")

    elif choice == '4':
        if not grades:
            print("No grades to sort.")
        else:
            order = input("Sort order (1 for ascending, 2 for descending): ").strip()
            if order == '1':
                grades.sort()
                print("Grades sorted in ascending order:", grades)
            elif order == '2':
                grades.sort(reverse=True)
                print("Grades sorted in descending order:", grades)
            else:
                print("Invalid sort option.")

    elif choice == '5':
        if grades:
            print("All grades:", grades)
        else:
            print("No grades to display.")

    elif choice == '6':
        print("Exiting Student Grade Tracker. Goodbye!")
        break

    else:
        print("Invalid option. Please choose a number between 1 and 6.")
