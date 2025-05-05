grades = []

def student_grades():
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
            add_marks(grades)
            print("the grades =",grades)
        elif choice == '2':
            print("")
            #remove_grade(grades)
        elif choice == '3':
            print("")
            #show_statistics(grades)
        elif choice == '4':
            print("")
            #sort_grades(grades)
        elif choice == '5':
            print("")
            #display_grades(grades)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Choose between 1-6.")

def add_marks(grades):
    grade_input = input("Enter a grade (0-100): ")
    if grade_input.isdigit():
        grade = int(grade_input)
        if 0 <= grade <= 100:
            grades.append(grade)
            print("Grade added successfully!")
        else:
            print("Grade must be between 0 and 100.")
    else:
        print("Invalid input. Please enter a numeric grade.")


student_grades()
