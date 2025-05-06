grades = []
def add_grade():
    grade_input = input("Enter a grade (0-100): ")
        
# .isdigit() for input checking
    if grade_input.isdigit():
        grade = int(grade_input)
        if 0 <= grade <= 100:
            grades.append(grade)
            print("Grade added successfully!")
        else:
            print("Grade must be between 0 and 100.")
    else:
        print("Invalid input. Please enter a number 0-100")

def remove_grade():
    grade_input = input("Enter the grade to remove: ")
    if grade_input.isdigit():
        grade = int(grade_input)
        if grade in grades:
            grades.remove(grade)
            print("Grade removed successfully!")
        else:
            print("Grade is not found.")
    else:
        print("Invalid input. Please enter a number 0-100")

def show_statistics():
    if grades:
        average = sum(grades) / len(grades)
        print("Statistics:")
        print("Average:", average)
        print(f"Minimum: {min(grades)}")
        print(f"Maximum: {max(grades)}")
    else:
        print("No grades available to show statistics.")

def sort_grades():
    if not grades:
        print("No grades to sort.")
        return
    order = input("Sort order (1 for ascending, 2 for descending): ")
    if order == "1":
        sorted_grades = sorted(grades)
        print(f"Grades sorted in ascending order: {sorted_grades}")
    elif order == "2":
        sorted_grades = sorted(grades, reverse=True)
        print(f"Grades sorted in descending order: {sorted_grades}")
    else:
        print("Invalid sort option.")

def display_grades():
    if grades:
        print("All grades:", grades)
    else:
        print("No grades to display.")

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
        add_grade()
    elif choice == "2":
        remove_grade()
    elif choice == "3":
        show_statistics()
    elif choice == "4":
        sort_grades()
    elif choice == "5":
        display_grades()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please choose from 1 to 6.")