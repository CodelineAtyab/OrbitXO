grades = []
print("Welcome to the Student Grade Tracker!")
running = True
while running:
    print("\nMenu:")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. Show statistics")
    print("4. Sort grades")
    print("5. Display all grades")
    print("6. Exit")
    choice = input("Choose an option (1-6): ")
    if choice == '1':
        grade = input("Enter a grade (0-100): ")
        if grade.isdigit():
            grade = int(grade)
            if 0 <= grade <= 100:
                grades.append(grade)
                print("Grade added successfully!")
            else:
                print("Grade must be between 0 and 100.")
        else:
            print("Please enter a valid number.")
    elif choice == '2':
        if not grades:
            print("No grades to remove.")
        else:
            print("Grades:", grades)
            print("Remove by:")
            print("1. By value")
            print("2. By index")
            remove_choice = input("Choose 1 or 2: ")
            if remove_choice == '1':
                value = input("Enter grade value to remove: ")
                if value.isdigit():
                    value = int(value)
                    if value in grades:
                        grades.remove(value)
                        print("Grade removed.")
                    else:
                        print("Grade not found.")
                else:
                    print("Please enter a number.")
            elif remove_choice == '2':
                index = input("Enter grade index to remove: ")
                if index.isdigit():
                    index = int(index)
                    if 0 <= index < len(grades):
                        removed_grade = grades.pop(index)
                        print("Removed grade:", removed_grade)
                    else:
                        print("Invalid index.")
                else:
                    print("Please enter a number.")
            else:
                print("Invalid choice.")
    elif choice == '3':
        if not grades:
            print("No grades to show statistics.")
        else:
            avg = sum(grades) / len(grades)
            minimum = min(grades)
            maximum = max(grades)
            print("Statistics:")
            print("Average:", round(avg, 2))
            print("Minimum:", minimum)
            print("Maximum:", maximum)
    elif choice == '4':
        if not grades:
            print("No grades to sort.")
        else:
            print("Sort order:")
            print("1. Ascending")
            print("2. Descending")
            sort_choice = input("Choose 1 or 2: ")
            if sort_choice == '1':
                grades.sort()
                print("Grades sorted ascending:", grades)
            elif sort_choice == '2':
                grades.sort(reverse=True)
                print("Grades sorted descending:", grades)
            else:
                print("Invalid choice.")
    elif choice == '5':
        if not grades:
            print("No grades to display.")
        else:
            print("All grades:", grades)
    elif choice == '6':
        print("Exiting. Goodbye!")
        running = False
    else:
        print("Invalid option. Please select between 1 and 6.")