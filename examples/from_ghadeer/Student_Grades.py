grades = []

def show_menu():
    print("\nStudent Grade Tracker")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. Show statistics")
    print("4. Sort grades")
    print("5. Show all grades")
    print("6. Exit")

while True:
    show_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        grade = input("Enter a grade (0-100): ")
        if grade.isdigit():
            grade = int(grade)
            if 0 <= grade <= 100:
                grades.append(grade)
                print("Grade added!")
            else:
                print("Grade must be between 0 and 100.")
        else:
            print("Please enter a number.")
    
    elif choice == "2":
        if grades:
            grade = input("Enter the grade to remove: ")
            if grade.isdigit():
                grade = int(grade)
                if grade in grades:
                    grades.remove(grade)
                    print("Grade removed!")
                else:
                    print("Grade not found.")
            else:
                print("Please enter a number.")
        else:
            print("No grades to remove.")
    
    elif choice == "3":
        if grades:
            average = sum(grades) / len(grades)
            print("Statistics:")
            print("Average:", average)
            print("Minimum:", min(grades))
            print("Maximum:", max(grades))
        else:
            print("No grades to show.")
    
    elif choice == "4":
        if grades:
            order = input("Sort order (1 for ascending, 2 for descending): ")
            if order == "1":
                grades.sort()
                print("Grades sorted:", grades)
            elif order == "2":
                grades.sort(reverse=True)
                print("Grades sorted:", grades)
            else:
                print("Invalid choice.")
        else:
            print("No grades to sort.")
    
    elif choice == "5":
        print("All grades:", grades)
    
    elif choice == "6":
        print("Goodbye!")
        break
    
    else:
        print("Invalid option. Try again.")
