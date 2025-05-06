

def student_grades():
    grades = []
    while True:
        print("\nStudent Grade Tracker")
        print("1. Add grade")
        print("2. Remove grade")
        print("3. Show statistics")
        print("4. Sort grades")
        print("5. Display all grades")
        print("6. Exit")

        choice = input("\nChoose an option: ")
        if choice == '1':
            add_grade(grades)
            print("the grades =",grades)
        elif choice == '2':
            print("")
            remove_grade(grades)
        elif choice == '3':
            print("")
            show_statistics(grades)
        elif choice == '4':
            print("")
            sort_grades(grades)
        elif choice == '5':
            print("")
            display_grades(grades)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Choose between 1-6.")

def add_grade(grades):
    grade_input = input("Enter grade(s) (0-100), separated by spaces: ")
    entries = grade_input.split()
    
    for entry in entries:
        if entry.isdigit():
            grade = int(entry)
            if 0 <= grade <= 100:
                grades.append(grade)
                print(f"Grade {grade} added successfully!")
            else:
                print(f"Grade {grade} is out of range (0-100). Not added.")
                
        else:
            print(f"'{entry}' is not a valid number. Skipped.")
            
    if not entries:
        print("No valid grades entered.")

def remove_grade(grades):
    if not grades:
        print("no grades ")
        return
    method=input("Remove by (v)alue or (i)ndex?").lower()
    if method == "v":
        remov_val:int = input("Enter grade value to remove: ")
        if remov_val.isdigit():
            val = int(remov_val)
            if val in grades:
                grades.remove(val)
                print("Grade removed.")
            else:
                print("Grade not found.")
        else:
            print("Invalid input.")

    elif method == 'i':
        remov_idx:int  = input("Enter index to remove: ")
        if remov_idx.isdigit():
            indx=int(remov_idx)
            if 0 <= indx < len(grades):
                removed = grades.pop(indx)
                print(f"Removed grade: {removed}")
            else:
                print("Invalid index.")
        else:
              print("Invalid input.")
    else:
        print("Invalid choice.")

def show_statistics(grades):
    if not grades:
        print("No grades available.")
        return
    print("Statistics:")
    print(f"Average: {sum(grades)/len(grades):.2f}")
    print(f"Minimum: {min(grades)}")
    print(f"Maximum: {max(grades)}")


def sort_grades(grades):
    if not grades:
        print("No grades to sort.")
        return
    grades.sort()
    print(f"Grades sorted: {grades}")

    grades.sort(reverse=True)
    print(f"Grades sorted: {grades}")

def display_grades(grades):
    if grades:
        print("All grades:", grades)
    else:
        print("No grades entered.")

student_grades()

