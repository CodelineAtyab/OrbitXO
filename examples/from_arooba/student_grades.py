grades = []  # This list will store all the grades

# Main menu loop
while True:
    print("\nStudent Grade Tracker")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. Show statistics")
    print("4. Sort grades")
    print("5. Display all grades")
    print("6. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        grade = int(input("Enter a grade (0-100): "))
        if grade >= 0 and grade <= 100:
            grades.append(grade)
            print("Grade added!")
        else:
            print("Grade must be between 0 and 100.")

    elif choice == "2":
        grade = int(input("Enter the grade to remove: "))
        if grade in grades:
            grades.remove(grade)
            print("Grade removed!")
        else:
            print("Grade not found.")

    elif choice == "3":
        if len(grades) > 0:
            total = sum(grades)
            average = total / len(grades)
            print("Statistics:")
            print("Average:", average)
            print("Minimum:", min(grades))
            print("Maximum:", max(grades))
        else:
            print("No grades to show.")

    elif choice == "4":
        if len(grades) == 0:
            print("No grades to sort.")
        else:
            print("1. Ascending")
            print("2. Descending")
            order = input("Choose sort order (1 or 2): ")
            if order == "1":
                grades.sort()
                print("Grades sorted:", grades)
            elif order == "2":
                grades.sort(reverse=True)
                print("Grades sorted:", grades)
            else:
                print("Invalid choice.")

    elif choice == "5":
        if len(grades) > 0:
            print("All grades:", grades)
        else:
            print("No grades to show.")

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please choose from 1 to 6.")
