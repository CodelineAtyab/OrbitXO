grades = []

while True:
    print("\nStudent Grade Tracker")
    print("1. Add grades")
    print("2. Remove grade")
    print("3. Show statistics")
    print("4. Sort grades")
    print("5. Display all grades")
    print("6. Exit") 

    choice = input("Choose an option (1-6): ")

    if choice == "1":
        grade_input = input("Enter grades separated by spaces (0-100): ")
        grade_list = grade_input.split()

        for g in grade_list:
            if g.isdigit():
                grade = int(g)
                if 0 <= grade <= 100:
                    grades.append(grade)
                else:
                    print(f"{grade} is out of range. Only 0–100 allowed.")
            else:
                print(f"'{g}' is not a valid number and was skipped.")
        print("Grades added successfully!")

    elif choice == "2":
        print("Remove by:")
        print("1. Grade value")
        print("2. Index")
        remove_choice = input("Choose an option: ")

        if remove_choice == "1":
            value = input("Enter the grade to remove: ")
            if value.isdigit():
                value = int(value)
                if value in grades:
                    grades.remove(value)
                    print("Grade removed.")
                else:
                    print("Grade not found.")
            else:
                print("Please enter a number.")

        elif remove_choice == "2":
            index = input("Enter the index to remove: ")
            if index.isdigit():
                index = int(index)
                if 0 <= index < len(grades):
                    removed = grades.pop(index)
                    print("Removed grade:", removed)
                else:
                    print("Invalid index.")
            else:
                print("Please enter a number.")

        else:
            print("Invalid choice.")

    elif choice == "3":
        if len(grades) == 0:
            print("No grades to show.")
        else:
            average = sum(grades) / len(grades)
            print("Statistics:")
            print("Average:", round(average, 2))
            print("Minimum:", min(grades))
            print("Maximum:", max(grades))

    elif choice == "4":
        if len(grades) == 0:
            print("No grades to sort.")
        else:
            print("Sort order:")
            print("1. Ascending")
            print("2. Descending")
            sort_choice = input("Choose sort order: ")

            if sort_choice == "1":
                grades.sort()
                print("Grades sorted (ascending):", grades)
            elif sort_choice == "2":
                grades.sort(reverse=True)
                print("Grades sorted (descending):", grades)
            else:
                print("Invalid sort option.")

    elif choice == "5":
        if len(grades) == 0:
            print("No grades yet.")
        else:
            print("Grades:", grades)

    elif choice == "6":
        print("Thank you for using the Student Grade Tracker!")
        break

    else:
        print("Invalid option. Please enter a number between 1 and 6.")
